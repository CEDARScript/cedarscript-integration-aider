# CEDARScript Integration: Aider

[![PyPI version](https://badge.fury.io/py/cedarscript-integration-aider.svg)](https://pypi.org/project/cedarscript-integration-aider/)
[![Python Versions](https://img.shields.io/pypi/pyversions/cedarscript-integration-aider.svg)](https://pypi.org/project/cedarscript-integration-aider/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`CEDARScript Integration: Aider` enables [`Aider`](https://aider.chat/) to use 
[**CEDARScript**](https://github.com/CEDARScript/cedarscript-grammar#readme)
as an [_edit format_](https://aider.chat/docs/benchmarks.html#edit-formats).

## Table of Contents
- [What is CEDARScript?](#what-is-cedarscript)
- [Installation](#how-to-use-it)
- [Usage](#usage)
- [Why Use CEDARScript?](#why-use-cedarscript)
- [Performance Comparison](#performance-comparison)
- [Individual Test Analysis](#individual-test-analysis)
- [Detailed Analysis](#detailed-analysis)
- [Contributing](#contributing)
- [License](#license)

## What is CEDARScript?

[CEDARScript](https://github.com/CEDARScript/cedarscript-grammar#readme) (_Concise Examination, Development, And Refactoring Script_)
is a domain-specific language designed to improve how AI coding assistants interact with codebases and communicate their code modification intentions.
It provides a standardized way to express complex code modification and analysis operations, making it easier for
AI-assisted development tools to understand and execute these tasks.

## How to use it

1. [Install Aider](https://aider.chat/docs/install.html), if you haven't.
2. Now, simply use the [`--edit-format` switch](https://aider.chat/docs/more/edit-formats.html) and select `cedarscript`:
```shell
aider --model gemini/gemini-1.5-flash-latest --edit-format cedarscript
```

## Why use CEDARScript?

`TL;DR`: You can get higher success rates when compared to other edit formats.

1. **Higher Success Rates**: Significantly improves the performance of AI models in code refactoring tasks.
2. **Cost-Effective Performance**: Enables more affordable models to compete with top-tier options.
3. **Standardized Communication**: Provides a consistent format for AI-code interaction in coding tasks.
4. **Enhanced Accuracy**: Reduces errors and improves the quality of AI-generated code modifications.

## Performance Comparison

CEDARScript has shown remarkable improvements in AI model performance for code refactoring:

| Model             | Format      | Pass Rate | Well-Formed Cases | Syntax Errors | Indentation Errors | Cost | Avg. Time per case |
|-------------------|-------------|-----------|-------------------|---------------|--------------------|------|--------------------|
| Gemini 1.5 PRO    | CEDARScript | 77.5%     | 86.5%             | 4             | 3                  | 26.2 | 29                 |
| Gemini 1.5 Flash  | CEDARScript | 76.4%     | 94.4%             | 3             | 5                  | 0.68 | 14.7               |
| Claude 3.5 Sonnet | diff        | 64.0%     | 76.4%             | n/a           | n/a                | n/a  | n/a                |
| Gemini 1.5 PRO    | diff-fenced | 49.4%     | 7.9%              | 21            | 93                 | 28.3 | 110.1              |

### Notable Achievements:
- **Gemini 1.5 _PRO_** with **CEDARScript** outperformed both its diff-fenced format and **Claude 3.5 Sonnet**.
- Most remarkably, the more cost-effective **Gemini 1.5 _Flash_** model, using **CEDARScript**, outperformed **Claude 3.5 Sonnet**.
  - It goes to show that even a more affordable model can surpass top-tier competitors when equipped with the _right_ tools.

This suggests that **CEDARScript** can level the playing field, enabling more accessible AI models
to compete with and even _exceed_ the capabilities of more expensive options in certain coding tasks.


### Individual Test Analysis

**Overall Performance**

|             | Count | %     |
|-------------|-------|-------|
| Improved    | 39    | 43.8% |
| Worsened    | 7     | 7.9%  |
| Stable      | 43    | 48.3% |
| Total tests | 89    | 100%  |

<details>
<summary>Individual Test Diff</summary>

```diff
--- 2024-10-22-05-21-41--gemini-1.5-flash-refactoring-whole
+++ 2024-10-22-05-13-37--gemini-1.5-flash-refactoring-cedarscript-i0.0.9-e0.3.3
# ============= Failed Attempts per Test =============
# N >= 0: it eventually passed after N failed attempts
# N < 0 : All attempts failed and limit was reached

@@ Improved, now PASSED (36) @@
++analyzer_cli_DebugAnalyzer__make_source_table: -4 -> 0
++autodetector_MigrationAutodetector__trim_to_apps: -4 -> 0
++backends_ModelBackend_with_perm: -4 -> 0
++builtin_BuiltinVariable_call_setattr: -4 -> 0
++checks_BaseModelAdminChecks__check_ordering_item: -4 -> 0
++checks_BaseModelAdminChecks__check_raw_id_fields_item: -4 -> 0
++checks_ModelAdminChecks__check_action_permission_methods: -4 -> 0
++checks_ModelAdminChecks__check_inlines_item: -4 -> 0
++checks_ModelAdminChecks__check_list_display_item: -4 -> 0
++clustering_ops_KMeans__mini_batch_training_op: -4 -> 0
++codeeditor_CodeEditor___get_brackets: -4 -> 0
++config_AppConfig__path_from_module: -4 -> 0
++config_ConfigCLI__get_settings_vars: -4 -> 0
++coordinator_HERETransitDataUpdateCoordinator__parse_transit_response: -4 -> 0
++cuda_cpp_scheduling_CUDACPPScheduling__can_fuse_epilogue_impl: -4 -> 0
++dataframeeditor_DataFrameView_next_index_name: -4 -> 0
++diffsettings_Command_output_hash: -4 -> 0
++dim2_Dim2CompatTests_test_reductions_2d_axis0: -4 -> 3
++distribution_DistributionFiles_parse_distribution_file_SUSE: -4 -> 0
++doc_DocCLI_get_role_man_text: -4 -> 0
++figure_FigureBase_colorbar: -4 -> 0
++functional_Functional__conform_to_reference_input: -4 -> 0
++galaxy_GalaxyCLI_execute_list_collection: -4 -> 0
++kernel_SpyderKernel_get_fault_text: -4 -> 1
++main_widget_PylintWidget_parse_output: -4 -> 0
++methods_BaseMethodsTests_test_where_series: -4 -> 0
++ogrinspect_Command_add_arguments: -4 -> 0
++onnxfunction_dispatcher_OnnxFunctionDispatcher__get_aten_name: -4 -> 1
++operations_DatabaseOperations_last_executed_query: -4 -> 0
++polar_RadialTick__determine_anchor: -4 -> 0
++profile_analyzer_cli_ProfileAnalyzer__get_list_profile_lines: -4 -> 0
++split_cat_SplitCatSimplifier_replace_cat: -4 -> 0
++split_cat_SplitCatSimplifier_replace_split: -4 -> 0
++text_CountVectorizer__limit_features: -4 -> 0
++triton_TritonScheduling_define_kernel: -4 -> 0
++triton_TritonScheduling_generate_node_schedule: -4 -> 0

@@ Improved, minor (3) @@
+ checks_BaseModelAdminChecks__check_autocomplete_fields_item: 3 -> 0
+ dataloader_DataLoader__is_role: 2 -> 0
+ operations_OracleOperations_convert_extent: 1 -> 0

@@ Worsened, now FAILED (7) @@
--base_BaseHandler_adapt_method_mode: 0 -> -4
--feedgenerator_Atom1Feed_add_item_elements: 0 -> -4
--generic_bsd_GenericBsdIfconfigNetwork_parse_inet_line: 0 -> -4
--graph_drawer_FxGraphDrawer__stringify_tensor_meta: 0 -> -4
--group_batch_fusion_GroupLinearFusion_fuse: 0 -> -4
--inspectdb_Command_normalize_col_name: 0 -> -4
--introspection_DatabaseIntrospection__parse_column_or_constraint_definition: 0 -> -4

@@ Stable: PASSED (30) @@
=+autosave_AutosaveForPlugin_get_files_to_recover: 0
=+base_BaseHandler_check_response: 0
=+baseconv_BaseConverter_convert: 0
=+compile_utils_MetricsContainer__get_metric_object: 0
=+concat__Concatenator__clean_keys_and_objs: 0
=+config_NetworkConfig_parse: 0
=+csrf_CsrfViewMiddleware__set_csrf_cookie: 0
=+dumpdata_Command_add_arguments: 0
=+finders_FileSystemFinder_check: 0
=+gateway_Gateway_get_and_delete_all_sms: 0
=+getitem_BaseGetitemTests_test_get: 0
=+grad_scaler_GradScaler__unscale_grads_: 0
=+gradient_checker_GradientChecker__assertInferTensorChecks: 0
=+graph_MigrationGraph_iterative_dfs: 0
=+grpc_debug_server_EventListenerBaseServicer__process_tensor_event_in_chunks: 0
=+i18n_JavaScriptCatalog_get_paths: 0
=+inspectdb_Command_get_field_type: 0
=+inspectdb_Command_get_meta: 0
=+introspection_DatabaseIntrospection__get_column_collations: 0
=+load_v1_in_v2__EagerSavedModelLoader__extract_signatures: 0
=+makemessages_Command_add_arguments: 0
=+makemigrations_Command_add_arguments: 0
=+migrate_Command_add_arguments: 0
=+operations_DatabaseOperations_bulk_insert_sql: 0
=+operations_DatabaseOperations_check_expression_support: 0
=+reshaping_BaseReshapingTests_test_concat_mixed_dtypes: 0
=+schema_DatabaseSchemaEditor_quote_value: 0
=+shell_Command_python: 0
=+special_RunSQL__run_sql: 0
=+weather_NWSWeather__forecast: 0

@@ Stable: FAILED (13) @@
=-autodetector_MigrationAutodetector_check_dependency: -4 -> -4
=-checks_ModelAdminChecks__check_list_editable_item: -4 -> -4
=-common_methods_invocations_foreach_inputs_sample_func__sample_rightmost_arg: -4 -> -4
=-common_utils_TestCase_genSparseTensor: -4 -> -4
=-doc_DocCLI_display_plugin_list: -4 -> -4
=-generator_GenOpTestCase_out_variant_op_test_case_generator: -4 -> -4
=-options_ModelAdmin_message_user: -4 -> -4
=-patches__Curve__get_arrow_wedge: -4 -> -4
=-quiver_Barbs__make_barbs: -4 -> -4
=-reshaping_BaseReshapingTests_test_unstack: -4 -> -4
=-sharding_policies_MaxShardSizePolicy__add_partition: -4 -> -4
=-split_cat_SplitCatSimplifier_get_transform_params: -4 -> -4
=-symbolic_shapes_ShapeEnv_bind_symbols: -4 -> -4

# =============          TOTALS          =============
# IMPROVED: 39
#    Now PASSES: 36
#    Minor     : 3
# WORSENED: 7
#    Now FAILED: 7
#    Minor     : 0
# STABLE  : 43
#    PASSED: 30
#    FAILED: 13
# TOTAL  : 89
```
</details>

#### Detailed Analysis

This overview suggests that the CEDARScript edit format has had a significant positive impact on the task of method extraction,
with improvements in nearly half of the tests and only a small percentage of tests worsening.

**Improvements:**

36 tests that previously failed now pass. This is a substantial improvement, indicating that CEDARScript is more 
effective in correctly extracting methods from classes across a wide range of codebases.

**Notable improvements include:**
- `analyzer_cli_DebugAnalyzer__make_source_table`: Suggests better handling of debug-related code refactoring.
- `autodetector_MigrationAutodetector__trim_to_apps`: Indicates improved capability in refactoring Django migration-related code.
- `cuda_cpp_scheduling_CUDACPPScheduling__can_fuse_epilogue_impl`: Shows better performance in handling complex CUDA-related code.
- `triton_TritonScheduling_define_kernel` and triton_TritonScheduling_generate_node_schedule: Demonstrates improved capability in refactoring GPU computing-related code.

**Minor Improvements:**

3 tests showed minor improvements, such as `checks_BaseModelAdminChecks__check_autocomplete_fields_item`, suggesting 
slight enhancements in handling Django admin-related code.

**Regressions:**

7 tests that previously passed now fail. While concerning, it's a relatively small number compared to the improvements.

**Notable regressions include:**
- `feedgenerator_Atom1Feed_add_item_elements`: Suggests potential issues with refactoring feed generation code.
- `generic_bsd_GenericBsdIfconfigNetwork_parse_inet_line`: Indicates challenges in refactoring network-related parsing code.
- `introspection_DatabaseIntrospection__parse_column_or_constraint_definition`: Shows difficulties in handling database schema introspection code.

**Stability:**

30 tests remained stable and passing, indicating that CEDARScript maintained performance in many areas, including various 
Django commands, database operations, and utility functions.
13 tests remained stable but failing, suggesting that some challenging areas were not addressed by either format.
These include complex operations like `symbolic_shapes_ShapeEnv_bind_symbols` and `reshaping_BaseReshapingTests_test_unstack`.

**Analysis by Domain:**

- **Web Frameworks (e.g., Django)**: Generally improved, with better handling of model admin checks, configuration, and 
database operations.
- **Data Science and ML**: Mixed results. Improvements in areas like clustering operations (`clustering_ops_KMeans__mini_batch_training_op`)
and data frame handling, but persistent issues in some reshaping operations.
- **System-level Operations**: Some improvements (e.g., `distribution_DistributionFiles_parse_distribution_file_SUSE`)
but also regressions (e.g., `generic_bsd_GenericBsdIfconfigNetwork_parse_inet_line`).
- **GPU and High-Performance Computing**: Significant improvements, especially in `CUDA` and `Triton`-related code.

**Interpretation:**

CEDARScript appears more effective in handling complex code structures, especially in areas related to web frameworks, 
data processing, and high-performance computing.
It shows improved capability in understanding class contexts and correctly extracting methods across various domains.
However, it may introduce new challenges in certain specific areas, possibly due to its different approach to code manipulation.

**Areas for Further Investigation:**

Understanding why certain tests regressed (e.g., `feedgenerator_Atom1Feed_add_item_elements`) could provide insights for improvement.

Analyzing the stable failing tests (e.g., `symbolic_shapes_ShapeEnv_bind_symbols`) to see if CEDARScript can be enhanced 
to address these persistent issues.

**Conclusion:**
- The introduction of CEDARScript appears to be a significant improvement for the task of extracting methods from classes.
- It shows particular strength in handling complex codebases, especially those related to web frameworks, data processing, and high-performance computing.
- However, care should be taken to address the areas where regressions occurred, particularly in system-level operations and certain parsing tasks.
- The consistent performance across various domains suggests that CEDARScript offers a more robust and versatile approach to code refactoring.

This analysis indicates that CEDARScript is a promising enhancement to Aider, offering more accurate and comprehensive 
method extraction capabilities across a wide range of codebases.
However, it also highlights the need for continued refinement, especially in areas where regressions were observed.
</details>

### Benchmark Metrics

<details>
<summary>Sonnet 3.5 + diff</summary>

```yaml
- dirname: refac-claude-3.5-sonnet-diff-not-lazy
  model: claude-3.5-sonnet (diff)
  edit_format: diff
  pass_rate_1: 64.0
  percent_cases_well_formed: 76.4
```
</details>

<details>
<summary>Gemini 1.5 PRO + diff-fenced (leaderboard site)</summary>

```yaml
- dirname: refac-gemini
  model: gemini/gemini-1.5-pro-latest
  edit_format: diff-fenced
  pass_rate_1: 49.4
  percent_cases_well_formed: 7.9
```
</details>

<details>
<summary>Gemini 1.5 PRO + diff-fenced (own tests)</summary>

```yaml
- dirname: 2024-10-05-00-43-21--diff-fenced-Gemini-Refactoring
  test_cases: 89
  model: gemini/gemini-1.5-pro-latest
  edit_format: diff-fenced
  commit_hash: 772710b-dirty
  pass_rate_1: 18.0
  pass_rate_2: 21.3
  pass_rate_3: 24.7
  percent_cases_well_formed: 34.8
  error_outputs: 180
  num_malformed_responses: 180
  num_with_malformed_responses: 58
  user_asks: 128
  lazy_comments: 2
  syntax_errors: 21
  indentation_errors: 93
  exhausted_context_windows: 0
  test_timeouts: 0
  command: aider --model gemini/gemini-1.5-pro-latest
  date: 2024-10-05
  versions: 0.57.2.dev
  seconds_per_case: 110.1
  total_cost: 28.2515
```
</details>

<details>
<summary>Gemini 1.5 PRO + CEDARScript</summary>

```yaml
- dirname: 2024-10-19-22-48-07--cedarscript-0.3.1-refactoring-gemini1.5pro
  test_cases: 89
  model: gemini/gemini-1.5-pro-latest
  edit_format: cedarscript-g
  commit_hash: 4da1e9b-dirty
  pass_rate_1: 77.5
  percent_cases_well_formed: 86.5
  error_outputs: 337
  num_malformed_responses: 19
  num_with_malformed_responses: 12
  user_asks: 12
  lazy_comments: 0
  syntax_errors: 4
  indentation_errors: 3
  exhausted_context_windows: 0
  test_timeouts: 0
  command: aider --model gemini/gemini-1.5-pro-latest
  date: 2024-10-19
  versions: 0.59.2.dev
  seconds_per_case: 29.0
  total_cost: 26.2374
```
</details>

<details>
<summary>Gemini 1.5 Flash + whole</summary>

```yaml
- dirname: 2024-10-22-05-21-41--gemini-1.5-flash-refactoring-whole
  test_cases: 89
  model: gemini/gemini-1.5-flash-002
  edit_format: whole
  commit_hash: feb1c38
  pass_rate_1: 41.6
  pass_rate_2: 42.7
  pass_rate_3: 43.8
  pass_rate_4: 44.9
  percent_cases_well_formed: 100.0
  error_outputs: 0
  num_malformed_responses: 0
  num_with_malformed_responses: 0
  user_asks: 558
  lazy_comments: 28
  syntax_errors: 106
  indentation_errors: 20
  exhausted_context_windows: 0
  test_timeouts: 0
  command: aider --model gemini/gemini-1.5-flash-002
  date: 2024-10-22
  versions: 0.59.2.dev
  seconds_per_case: 231.1
  total_cost: 2.3894
```
</details>

<details>
<summary>Gemini 1.5 Flash + CEDARScript</summary>

```yaml
- dirname: 2024-10-20-00-33-27--cedarscript-0.3.1-refactoring-gemini-1.5-flash
  test_cases: 89
  model: gemini/gemini-1.5-flash-latest
  edit_format: cedarscript-g
  commit_hash: 4da1e9b-dirty
  pass_rate_1: 76.4
  percent_cases_well_formed: 94.4
  error_outputs: 403
  num_malformed_responses: 13
  num_with_malformed_responses: 5
  user_asks: 21
  lazy_comments: 0
  syntax_errors: 3
  indentation_errors: 5
  exhausted_context_windows: 0
  test_timeouts: 0
  command: aider --model gemini/gemini-1.5-flash-latest
  date: 2024-10-20
  versions: 0.59.2.dev
  seconds_per_case: 14.7
  total_cost: 0.6757
```
</details>

#### functional_Functional__conform_to_reference_input

</details>

<details>
<summary>diff-fenced</summary>

```yaml
    "cost": 0.33188854999999995,
    "duration": 27.793912172317505,
    "test_timeouts": 0,
    "commit_hash": "772710b-dirty",
    "num_error_outputs": 2,
    "num_user_asks": 3,
    "num_exhausted_context_windows": 0,
    "num_malformed_responses": 2,
    "syntax_errors": 0,
    "indentation_errors": 3,
    "lazy_comments": 0,
```

</details>

<details>
<summary>cedarscript</summary>

```yaml
    "cost": 0.18178265,
    "duration": 11.176445960998535,
    "test_timeouts": 0,
    "commit_hash": "772710b-dirty",
    "num_error_outputs": 0,
    "num_user_asks": 1,
    "num_exhausted_context_windows": 0,
    "num_malformed_responses": 0,
    "syntax_errors": 0,
    "indentation_errors": 0,
    "lazy_comments": 0,
```

</details>


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
