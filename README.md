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


### Raw Metrics

<details>
<summary>**Sonnet 3.5 + `diff`**</summary>

```yaml
- dirname: refac-claude-3.5-sonnet-diff-not-lazy
  model: claude-3.5-sonnet (diff)
  edit_format: diff
  pass_rate_1: 64.0
  percent_cases_well_formed: 76.4
```
</details>

<details>
<summary>Gemini 1.5 PRO + `diff-fenced` (leaderboard site)</summary>

```yaml
- dirname: refac-gemini
  model: gemini/gemini-1.5-pro-latest
  edit_format: diff-fenced
  pass_rate_1: 49.4
  percent_cases_well_formed: 7.9
```
</details>

<details>
<summary>Gemini 1.5 PRO + `diff-fenced` (own tests)</summary>

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
<summary>Gemini 1.5 PRO + `CEDARScript`</summary>

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
<summary>Gemini 1.5 _Flash_ + `CEDARScript`</summary>

```yaml
- dirname: 2024-10-20-00-33-27--cedarscript-0.3.1-refactoring-gemini1.5flash
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
