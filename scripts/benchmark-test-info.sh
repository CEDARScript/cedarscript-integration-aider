#!/usr/bin/env bash

aider_results_to_cols() {
  jq -j '.model, " ", .edit_format, " ", .cost, " ", .duration, " ", .test_timeouts, " ", .num_error_outputs, " ", .num_user_asks, " ", .num_exhausted_context_windows, " ", .num_malformed_responses, " ", .syntax_errors, " ", .indentation_errors, " ", .lazy_comments' \
    "$1"
}

format_duration() {
    local seconds=$1
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        date -u -r $(printf "%.0f" "$seconds") +%H:%M:%S
    else
        # Linux
        date -u -d @$(printf "%.0f" "$seconds") +%H:%M:%S
    fi
}

extract_token_counts() {
    grep -i "^> Tokens:" | awk '
    BEGIN {
      total_sent = 0
      total_received = 0
    }
    {
      for (i=1; i<=NF; i++) {
        if ($i ~ /^sent[,.]?$/) {
            sent = $(i-1)
            if (sent ~ /k/) {
                gsub("k", "", sent)
                sent = sent * 1000
            } else if (sent ~ /m/) {
                gsub("m", "", sent)
                sent = sent * 1000000
            }
            total_sent += sent
        }
        if ($i ~ /^received[,.]?$/) {
            received = $(i-1)
            if (received ~ /k/) {
                gsub("k", "", received)
                received = received * 1000
            } else if (received ~ /m/) {
                gsub("m", "", received)
                received = received * 1000000
            }
            total_received += received
        }
      }
    }
    END {
        printf "%.0f %.0f\n", total_sent, total_received
    }'
}

benchmark_ls() {
    test "$1" || { echo "Usage: benchmark.ls <benchmark-run-dir>" ; return 1;}
    local benchmark_run_dir="$1"

    echo "# -dirname $(basename "$benchmark_run_dir") tests"
    echo 'failed-attempts (negative if all attempts failed), test-name, duration, sent_tokens, received_tokens, model, edit_format, cost, test_timeouts, num_error_outputs, num_user_asks, num_exhausted_context_windows, num_malformed_responses, syntax_errors, indentation_errors, lazy_comments'
    i=0 total_duration=0 total_failed_attempts=0 failed_test_count=0 total_sent_tokens=0 total_received_tokens=0
    while IFS= read -r -d '' aider_json_file; do
        (( i+=1 ))
        read sent_tokens received_tokens <<< "$(
          cat "$(dirname "$aider_json_file")"/.aider.chat.history.md | \
          extract_token_counts
        )"
        ((total_sent_tokens+=sent_tokens, total_received_tokens+=received_tokens))
        outcome="$(jq -rc '.tests_outcomes' "$aider_json_file" | tr -d '[]')"
        test "$outcome" = true && \
          attempts=0 || \
          attempts=$(echo "$outcome" | tr ',' '\n' | grep -c "false")
        ((total_failed_attempts+=attempts))
        dir_name="$(basename "$(dirname "$aider_json_file")")"
        # If no attempt succeeded, make 'attempts' negative and inc failed_test_count
        echo "$outcome" | grep -q "true" || \
            ((attempts=-attempts, failed_test_count+=1))
        aider_result_cols="$( aider_results_to_cols "$aider_json_file" )"
        read test_model test_edit_format test_cost test_duration test_timeouts test_num_error_outputs test_num_user_asks test_num_exhausted_context_windows test_num_malformed_responses test_syntax_errors test_indentation_errors test_lazy_comments \
          <<< "$(echo $aider_result_cols)"
        total_duration=$(awk "BEGIN {print $total_duration + $test_duration}")
        total_cost=$(awk "BEGIN {print $total_cost + $test_cost}")
        ((
        total_test_timeouts+=test_timeouts,
        total_num_error_outputs+=test_num_error_outputs,
        total_num_user_asks+=test_num_user_asks,
        total_num_exhausted_context_windows+=test_num_exhausted_context_windows,
        total_num_malformed_responses+=test_num_malformed_responses,
        total_syntax_errors+=test_syntax_errors,
        total_indentation_errors+=test_indentation_errors,
        total_lazy_comments+=test_lazy_comments
        ))
        printf '%2d, %-25s, %7.3f, %6d, %07d, %-25s, %-25s, %0.3f, %2d, %2d, %2d, %2d, %2d, %2d, %2d, %2d\n' \
        "$attempts" "$dir_name" $test_duration $sent_tokens $received_tokens \
          $test_model $test_edit_format $test_timeouts $test_num_error_outputs $test_num_user_asks $test_num_exhausted_context_windows \
          $test_num_malformed_responses $test_syntax_errors $test_indentation_errors $test_lazy_comments
    done < <(find "$benchmark_run_dir" -name '.aider.results.json' -print0 | sort -z)

    printf '=================\n'
    printf 'Duration         : %s\n' $(format_duration $total_duration)
    printf 'Success          : %03.1f%% ( %i / %i )\n' $((100 * (i-failed_test_count) / i)) $((i-failed_test_count)) $i
    printf '# duration_s, test_pass_count, test_failed_count, failed_attempts, total_sent_tokens, total_received_tokens,total_cost, total_test_timeouts, total_num_error_outputs, total_num_user_asks, total_num_exhausted_context_windows, total_num_malformed_responses, total_syntax_errors, total_indentation_errors, total_lazy_comments\n'
    printf '# %03.3f, %03d, %03d, %03d, %07d, %07d, %0.3f, %02d, %02d, %02d, %02d, %02d, %02d, %02d, %02d\n' $total_duration $((i-failed_test_count)) $failed_test_count $total_failed_attempts $total_sent_tokens $total_received_tokens \
      $total_cost $total_test_timeouts $total_num_error_outputs $total_num_user_asks $total_num_exhausted_context_windows $total_num_malformed_responses $total_syntax_errors $total_indentation_errors $total_lazy_comments
}

benchmark_ls "$@"
