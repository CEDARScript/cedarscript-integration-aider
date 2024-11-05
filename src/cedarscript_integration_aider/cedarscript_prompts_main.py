# flake8: noqa: E501

from .cedarscript_prompts_base import CEDARScriptPromptsBase


class CEDARScriptPromptsMain(CEDARScriptPromptsBase):

    def edit_format_name(self):
        return f"{super().edit_format_name()}"

    final_remarks = CEDARScriptPromptsBase.final_remarks_brain

    edit_format_training = """## CEDARScript Quick Reference Guide
It's a *SQL-like* language used to express code transformations (via DDL and DML Write commands) and
to help an LLM examine and understand the codebase (via DML Read-Only command).
<core-commands>
<DML>
# Read-only command
<syntax-high-level>
<dl>
<dt>SELECT <target> FROM <source> [WHERE <condition>] [LIMIT <n>];</dt>
<dd>Read-only command. Used to glean information about the code base being examined.</dd>
<dd>Use cases:
- Understanding code structure;
- Finding relevant files/classes/functions/variables that may deal with a certain topic
-- (ex.: if a user may want to find all places that deal with payments, search for 'payment')
- Displaying code elements to user
</dd>
</dl>
</syntax-high-level>

# Code Modification commands
<syntax-high-level>
<dl>
<dt>UPDATE <update-target> <update-action> [WITH <contents>];</dt>
<dd>The main CEDARScript UPDATE command structure. Square brackets denote optional parts.</dd>
<dd>Use cases:
- Creating or replacing classes, functions or other code in existing files/classes/functions etc
- Replacing specific lines of existing code
- Performing complex code transformations using refactoring patterns
- etc...
</dd>

# Where:

<dt>update-target: [<identifier_matcher> FROM] FILE "<path>"</dt>
<dd>Specifies what to update:
- Direct file update (FILE "path"); Sets *reference point* for *vertical positioning* to the first line in the file.
- A specific <identifier_matcher> FROM FILE "path"; Sets *reference point* for *vertical positioning* to the 
first line where the identifier is declared (function signature, etc)
</dd>
<dd>Sets *reference point* for *vertical positioning* (Context-Relative Line Numbers)</dd>

<dt>update-action: (<action-mos> | <action-region>)</dt>
<dd>Possible actions: DELETE | MOVE | INSERT | REPLACE</dd>
<dd>Sets *reference point* for *horizontal positioning* (Relative Indent Level)</dd>
<dd>The reference point is the term chosen for the (MOVE|INSERT|REPLACE) action</dd>

<dd>Optional specification of new content:
- <content_literal>: direct text using <relative-indent-level-string>
- <content_from_segment>: content taken from existing code
- <line_filter>: filters input lines
</dd>

<dt>action-mos   : ( <update_delete_region_clause> | MOVE <marker_or_segment> <update_move_clause_destination> | <insert_clause> WITH <contents> | <replace_region_clause> | WITH (<contents> | <line_filter>) )</dt>
<dd>Use when update-target is a FILE</dd>
<dt>action-region: ( <update_delete_region_clause> | MOVE <region_field>      <update_move_clause_destination> | <insert_clause> WITH <contents> | <replace_region_clause> | WITH (<contents> | <line_filter>))</dt>
<dd>Use when update-target is an <identifier_matcher></dd>

</dl>
</syntax-high-level>

<syntax-detailed>
<dl>

# 3 forms are valid:

1. <dt>UPDATE FILE "<path>" <action-mos></dt>
<dd>Sets *reference point* for *vertical positioning* to the first line in the file</dd>

2. <dt>UPDATE <identifier_matcher> FROM FILE "<path>" <action-region></dt>
<dd>Sets *reference point* for *vertical positioning* to the first line where the identifier is declared (function signature, etc)</dd>

3. <dt>UPDATE PROJECT REFACTOR LANGUAGE "<string>" WITH PATTERN '''<string>''' [WITH GOAL '''<string>''']</dt>
<dd>Only languages "Rope" (for Python codebases) and "Comby" (for any codebase) are supported</dd>
<dd>Used for advanced pattern-based refactorings on any kind of code or data format (as HTML or JSON)</dd>
<dd>LANGUAGE "Rope": Indirectly use the `Restructure` class in the 'Rope' refactoring library to perform complex code transformations using patterns</dd>
<dd>LANGUAGE "Comby": Use lightweight templates to easily search and change code or data formats. Comby is designed to work on any language or data format</dd>

# Where:

<dt>update_delete_region_clause: DELETE <region_field></dt>
<dd>Removes a region of code in a file</dd>

<dt>insert_clause: INSERT <relpos_bai></dt>
<dd>Specifies where content will be placed</dd>
<dd>Used as reference point for *horizontal positioning* only (*NOT* for vertical positioning)</dd>

<dt>replace_region_clause: REPLACE <region_field></dt>
<dd>Defines what region to be replaced</dd>
<dd>Used as reference point for `relative indent level` only (*NOT* for context-relative line numbers)</dd>

<dt>marker_or_segment: (<marker> | <segment>)</dt>
<dd></dd>
<dt>marker: (<line_with_offset> | <identifier_matcher>)</dt>
<dd></dd>

<dt>line_matcher: [LINE] ('''<string>''' | <context-relative-line-number> | REGEX r'''<regex>''' | PREFIX '''<string>''' | SUFFIX '''<string>''' | INDENT LEVEL <integer> | EMPTY)</dt>
<dd>Points to specific line. For all comparisons below, the matcher *only sees* a stripped version of the line
(that is, after stripping leading and trailing whitespace characters)</dd>
<dd>Possible arguments:
- <string>: its *stripped contents*, if it's unambiguous (don't use line content if the line appears multiple times);
- <context-relative-line-number>: This can help if other types failed;
- REGEX: a regular expression pattern matching the stripped line; *MUST* use a raw string (one that starts with r''')
- PREFIX: matches if the stripped line *begins* with a prefix (anchored to the start);
- SUFFIX: matches if the stripped line *ends* wiht a suffix (anchored to the end);
- INDENT LEVEL: line has specific indent level 
- EMPTY: matches if the stripped line is empty
</dd>

<dt>line_with_offset: <line_matcher> [OFFSET <offset>]</dt>
<dd>Points to a specific <line_matcher> - see <offset> below</dd>

<dt>identifier_matcher: (VARIABLE | FUNCTION | METHOD | CLASS) "[parent-chain.]<name>" [OFFSET <offset>]</dt>
<dd>Name of an identifier</dd>
<dd>If there are 2 or more with same name, prefixed it with its *parent chain* (names of its parents separated by a dot) to disambiguate it.
Another way to disambiguate is to use `OFFSET <n>` to pinpoint one.
</dd>
<dd>Tip: `OFFSET 0` == first match! Remember to use `OFFSET 0` when you want to specify the FIRST match/occurrence</dd>

<dt>parent-chain: string</dt>
<dd>A dot-separated list of parents to uniquely identify an <identifier></dd>
<dd>When a reference is ambiguous (multiple matches exist for it), it must be disambiguated. Parent chains are the BEST way to do that</dd>
<dd>Examples:
- "name" (no parent chain, matches at any nesting level, including at the top level)
- ".name" (only root in the chain (so it's anchored), only matches "name" if it's at the top level of the file)
- "C.name" (1 parent in the chain, matches "name" as long as "C" is a direct parent of it)
- "B.C.name" (2 parents in the chain, requires "B" to be a direct parent of "C", and "C" a direct parent of "name")
- ...
</dd>
<dt>offset: integer</dt>
<dd>Determines how many matches to skip</dd>
<dd>When a reference is ambiguous (multiple matches exist for it), it must be disambiguated. Setting an OFFSET is a way to do that</dd>
<dd>Examples:
OFFSET 0: FIRST match;
OFFSET 1: skips 1 matches, so points to the *2nd* match;
OFFSET 2: skips 2 matches, so points to the *3rd* match;
OFFSET n: skips n matches, thus specifies the (n+1)-th match;
</dd>
<dd>Examples with context:
- UPDATE FUNCTION "my_func" OFFSET 0  -- Explicitly target FIRST match
- UPDATE FUNCTION "my_func" OFFSET 1  -- Target SECOND match
</dd>

<dt>segment: SEGMENT <relpos_segment_start> <relpos_segment_end></dt>
<dd>Points to segment identified by a start and an end pointer</dd>

<dt>region_field: (BODY | WHOLE | <marker_or_segment>)</dt>
<dt>WHOLE: keyword</dt>
<dd>the whole chosen item</dd>

<dt>BODY: keyword</dt>
<dd>Only the function/method body (its *signature* is *NOT* considered)</dd>

<dt>relpos_segment_start: STARTING (<relpos_at> | <relpos_beforeafter>)</dt>
<dd></dd>

<dt>relpos_segment_end: ENDING (<relpos_at> | <relpos_beforeafter>)</dt>
<dd></dd>

<dt>relpos_at: AT <marker></dt>
<dd></dd>

<dt>relpos_beforeafter: (BEFORE | AFTER) <marker></dt>
<dd>Points to region immediately before or after <marker></dd>
<dt>relpos_into: INTO <identifier_matcher> (TOP | BOTTOM)</dt>
<dd>Points to inside `identifier_matcher` (either the body's TOP or BOTTOM region). The *horizontal reference point* is the body</dd>
<dd>Use cases: When inserting content (e.g. a docstring or a return statement) either at the TOP or BOTTOM of a function or class body</dd>

<dt>relpos_bai: (<relpos_beforeafter> | <relpos_into>)</dt>
<dd></dd>
<dt>relative_indentation: RELATIVE INDENTATION <relative-indent-level></dt>
<dd>The reference point for the horizontal positioning of <relative_indentation> is the <marker> in (<insert_clause> | <replace_region_clause>)</dd>

## Content Sources

<dt>contents: (<content_literal> | <content_from_segment> )</dt>

<dt>content_literal: CONTENT '''<relative-indent-level-string>'''</dt>
<dd>Examples and enclosing variations (single quote, double quote and raw):</dd>
<dd>CONTENT '''@0:return "x"''' -- if the content has *double* quotes (") inside, use the *single* quote variation (''')</dd>
<dd>CONTENT '''@-1:if a > 0:'''</dd>
<dd>CONTENT r'''
@0:return "x"
@-1:if a > 0:
@0:s = re.sub(r'[^\\w\\s-]', '', s)
'''</d>
<dd>CONTENT \"\"\"
@0:my_multiline_text = '''test
@1:multi
@1:line
@0'''
\"\"\" -- if the content has *single* quotes (') inside, use the double quote variation (\"\"\")</dd>
<dd>CONTENT '''
@0:class myClass:
@1:def myFunction(param):
@2:if param > 0:
@3:print("Positive")
@2:else:
@3:print("Non-positive")
@2:return param * 2
@0:class nextClass:
'''</dd>
<dd>CONTENT r'''s = re.sub(r"[^\\w\\s-]", "", s)''' -- best to be safe and always use the raw string variation (r''' or r\"\"\")</dd>
<dt>content_from_segment: [singlefile_clause] <marker_or_segment> [relative_indentation]</dt>
<dd></dd>

<dt>line_filter: (<case_stmt> | <ed_stmt>)</dt>
<dd>Sends input lines to a filter for transformation and returns the resulting lines</dd>

<dt>ed_stmt: ED r'''<string>'''</dt>
<dd>Executes a *GNU ed* (the UNIX line editor) script to transform input lines</dd>

<dt>case_stmt: CASE WHEN <line_matcher> THEN <case_action></dt>
<dd>This is the reliable and versatile `CASE WHEN...THEN` line filter.
Filters each input line according to `WHEN...THEN` pairs:</dd>
<dd>WHEN: A <line_matcher></dd>
<dd>THEN: Allows you to choose which *action* to take for its matched lines</dd>
<dd><content_literal> or <content_from_segment>: Replace with text (cannot use regex capture groups)</dd>

<dt>loop_control: (CONTINUE | BREAK)</dt>
<dd>BREAK: Stops processing the lines, leaving the rest of the lines untouched</dd>
<dd>REMOVE: Removes the line</dd>

<dt>case_action: ( <loop_control> | REMOVE [loop_control] | SUB r'''<regex>''' r'''repl''' [loop_control] | INDENT <integer> [loop_control] | (<content_literal> | <content_from_segment>) [loop_control] )
<dd>CONTINUE: Leaves the line as is and goes to the next</dd>
<dd>INDENT: Increases or decreases indent level. Only positive or negative integers</dd>
<dd>SUB: Substitutes *ONLY* the part of the line that matches <regex> with <repl> (regex capture groups enabled: \\1, \\2, etc).

<dl>Examples of substituting <regex> matches with `<repl>`:

<dt>Replace `self,` with `replacement_param: str,`</dt>
<dd>
<original-line>def function_name(self, param_to_keep_1: int, param_to_keep_2: str):</original-line>
<regex>r'''def function_name\\(self, param_to_keep_1: int, param_to_keep_2: str\\):'''</regex>
<repl>r'''def function_name(replacement_param: str, param_to_keep_1: int, param_to_keep_2: str):'''</repl>
<cedarscript>
UPDATE FUNCTION "function_name"
  FROM FILE "file.py"
REPLACE WHOLE WITH CASE
  WHEN REGEX r'''def function_name\\(''' THEN SUB
    r'''def function_name\\(self, param_to_keep_1: int, param_to_keep_2: str\\):'''
    r'''def function_name(replacement_param: str, param_to_keep_1: int, param_to_keep_2: str):'''
END;
</cedarscript>
<line-after-match-replacement>def function_name(replacement_param: str, param_to_keep_1: int, param_to_keep_2: str):</line-after-match-replacement>
</dd>

<dt>Remove references to `self` from function signature</dt>
<dd>
<original-line>def function_name(self, existing_params):</original-line>
<regex>r'''def function_name\\(self, existing_params\\):'''</regex>
<repl>r'''def function_name(existing_params):'''</repl>
<line-after-match-replacement>def function_name(existing_params):</line-after-match-replacement>
</dd>

<dt>Transform method call into function call and also prepend new parameter to the call</dt>
<dd>Notice how the rest of the line isn't matched; Only the part that was matched is replaced:
<original-line>calculation_result = self.calc(existing_params) + self.calc_too(1, 3)</original-line>
<regex>r'''(self\\.)(calc\\()'''</regex>
<repl>r'''\\2\\1new_member_arg, '''</repl>
<line-after-match-replacement>calculation_result = calc(self.new_member_arg, existing_params) + self.calc_too(1, 3)</line-after-match-replacement>
</dd>

<dt>Replace print calls with logging.info calls</dt>
<dd>Notice how the rest of the line isn't matched; Only the part that was matched is replaced:
<original-line>while true; begin; a += 1; print(a); end</original-line>
<regex>r'''print\\((.*)\\)'''</regex>
<repl>r'''logging.info(\\1)'''</repl>
<line-after-match-replacement>while true; begin; a += 1; logging.info(a); end</line-after-match-replacement>
</dd>

<dt>Convert list comprehension to for loop</dt>
<dd>
<original-line>squares = [x2 for x in range(10)]</original-line>
<regex>r'''\\[(.?) for (.?) in (.*)\\]'''</regex>
<repl>r'''squares = []\\nfor \\2 in \\3: squares.append(\\1)'''</repl>
<line-after-match-replacement>
squares = []
for x in range(10): squares.append(x2)
</line-after-match-replacement>
</dd>

</dl> # END of examples 
</dd> # END of SUB

<dt>regex: *MUST* use a raw string (one that starts with r''')</dt>
<dd>Matches a part of the line. <CRUCIAL>Only the part that was matched will be replaced by <repl>, keeping the rest of the line intact</CRUCIAL>
Allows regex capture groups by enclosing parts of the expression in parentheses (without escaping them);
To *match* parentheses, you *MUST* escape them as in the 2 examples below:
1. to match left parenthesis: \\(
2. to match right parenthesis: \\)

</dd>
<dt>repl: *MUST* use a raw string (one that starts with r''')</dt>
<dd>A replacement that can recover regex capture groups: \\1, \\2, etc.
*ONLY* replaces the part of the line that was matched by <regex>, keeping the rest of the line intact!
*DO NOT* escape parentheses inside <repl> !!!
</dd>

<dt>update_move_clause_destination: [TO FILE "<path>"] <insert_clause> [relative_indentation]</dt>

## Horizontal Positioning: Relative Indent Level

<dt>relative-indent-level-string: <relative-indent-prefix><line-1><newline>[<relative-indent-prefix><line-2><newline>]...</dt>
<dd>(... denotes repetition)</dd>
<dd>line-1, line-2 ... line-n is the actual content for each line</dd>
<dd>MUST be used when providing CONTENT blocks. Simplifies matching indentation with the existing code being changed</dd>
<dd>The CEDARScript runtime will handle the actual formatting and indentation in the target code file</dd>
<dt>relative-indent-prefix: @<relative-indent-level>:</dt>
<dt>relative-indent-level: integer</dt>
<dd>Determines *horizontal positioning* as a *relative* indent *level* compared to the *horizontal positioning reference point*
(the reference point is the <marker> chosen for the <update-action> (MOVE|INSERT|REPLACE))</dd>
<dd>The relative indent level *MUST* change logically with code structure:
- Increment when entering a nested block (if/for/while/try etc...);
- Decrement when exiting a nested block;
</dd>
<dd>Examples:
0: *Same* level as reference point;
1: one more indent level than reference point;
-1: one *less* indent level than reference point;
</dd>
<dd>NOTE: If you get `E999 IndentationError` message or any other indentation error, check that your relative indent levels 
follow these rules</dd>

## Vertical Positioning: Context-Relative Line Numbers
<dt>context-relative-line-number: integer</dt>
<dd>Determines *vertical positioning*. Represents the relative line number compared to the *vertical positioning reference point*
(the reference point is the target chosen for the <update-target> - either the file itself or a specific <identifier_matcher> in it)</dd>
<dd>Number 1 points to the *first* line of its reference point; 2 points to the second, ...</dd>
<dd>Number 0 points to the line that comes *BEFORE* its reference point; -1 points to 2 lines before, ...</dd>

</dl>
</syntax-detailed>

</DML>
<DDL>
CREATE FILE "<path>" WITH <content_literal>;
RM FILE "<path>";
MV FILE "<source>" TO "<target>";
</DDL>
</core-commands>

## Cookbook

<codebase>
```Makefile
.PHONY: all version play build test dist clean

all: clean build version test

version:
	git describe --tags
	python -m setuptools_scm
```

```a1.py
def a_def1(
    a,
    b
):
    return a + b

def a():
    def a_def2(a, b):
        return a + b
def b():
    def a_def2(a, b):
        return a + b
def a_def2():
    return "x"
```

```a2.py
class A:
    def a(self, a1, a2):
        c, d = self.b(a1x)
        # a2x is incorrect
        c, d = self.b(a2x)
        if a1 > 0:
            c = "x" + a1
        return 1,2
    def b(self, a1):
        c, d = self.b(a1x)
        # a2x is wrong
        c, d = self.b(a2x)
        if a1 > 0:
            c = "x" + a1
        return 1,2
```

```a3.py
class MyClass(NamedTuple):
    def __init__(self):
        instance_var_1: str = '4r3'
    def myFirstFunction(
        self, name: str,
        age: int
    ):
        if age > 70
            a = doSomething(name, age)
        return a + 5 + len(self.instance_var_1) * 7
    def middle(self):
        pass
    def anotherFunction(self, name: str, age: int):
        print("dummy...")
        b = checkVal(45, "strict", self.myFirstFunction(name, age), 8, "tops", "lops")
        bb = checkVal(7, "lax", self.myFirstFunction(name, age), 2, "bottom", 'lops')
        c = "x" + '"' + "'" + "z" + "lops"
        print("calc d...lops...")
        print("dummy...")
        d = checkVal(45, "strict", self.myFirstFunction(name, age), 8, "tops", \"\"\"lops\"\"\")
        print("calc dd...")

        
        print("takes longer...")
        print("dummy...")
        dd = checkVal(4455, "aasdf", '33se"asd',
          "strict", 8, 
          "tops", "xx", 'lops'
          '9"f', "as'df", self.myFirstFunction(name, age), 'lops')
        return b * 3
```
</codebase>

Consider the files in the codebase above and see the examples below.

<dl note="each 'dd' item gets a fresh copy of the codebase files">
<dt file="Makefile">Add `v` as an alias to `version`</dt>
<dd>
UPDATE FILE "Makefile"
REPLACE WHOLE WITH CASE
  WHEN REGEX r'''^\\.PHONY''' THEN SUB
    r'''version'''
    r'''version v'''
  WHEN REGEX r'''^version''' THEN SUB
    r'''^version'''
    r'''version v'''
END;
</dd>
<dd>
-- We can use a regex group reference (\\1) to be even more concise
UPDATE FILE "Makefile"
REPLACE WHOLE WITH CASE
  WHEN REGEX r'''^\\.PHONY''' THEN SUB
    r'''(version)'''
    r'''\\1 v'''
  WHEN REGEX r'''^version''' THEN SUB
    r'''^(version)'''
    r'''\\1 v'''
END;
</dd>

<dt file="a1.py">Add Docstring to a Python function/method/body</dt>
<dd>
-- Using `INTO .. TOP` is the *BEST* option to add content to the top of the body
-- The *reference point* for horizontal positioning is a_def1's body
UPDATE FILE "a1.py"
INSERT INTO FUNCTION "a_def1" TOP
WITH CONTENT r'''
@0:\"\"\"Calculate sum of two numbers.
@0:
@0:Args:
@1:a: First number
@1:b: Second number
@0:
@0:Returns:
@1:Sum of a and b
@0:\"\"\"
''';
</dd>
<dd>
-- We can also use `(AFTER|BEFORE) `LINE '''<string>'''`, which is still an excellent choice for this case.
-- Note: As the *reference point* for horizontal positioning is now line "):" instead of the body,
--   we need to use different values for the relative indent levels.
UPDATE FUNCTION "a_def1"
FROM FILE "a1.py"
INSERT AFTER LINE '''):'''
-- The CONTENT below uses line "):" (*not* the line after it) as reference point for horizontal positioning
WITH CONTENT r'''
@1:\"\"\"Calculate sum of two numbers.
@1:
@1:Args:
@2:a: First number
@2:b: Second number
@1:
@1:Returns:
@2:Sum of a and b
@1:\"\"\"
''';
</dd>

<dt file="a1.py">Disambiguate using parent chains</dt>
<dd>We cannot simply use `FUNCTION "a_def2"`, as it matches all 3 functions with that name.
We should use the `parent chain` to easily disambiguate it:</dd>
<dd>
-- Target the top-level a_def2
-- Starting the parent chain with a dot means we're anchoring the root (top level).
UPDATE FILE "a1.py"
INSERT INTO FUNCTION ".a_def2" TOP
WITH CONTENT r'''
@0:\"\"\"Returns a value\"\"\"
''';
</dd>
<dd>
-- Target a_def2 inside 'a'
-- Matches if a_def2 has 'a' as its immediate parent
UPDATE FILE "a1.py"
INSERT INTO FUNCTION "a.a_def2" TOP
WITH CONTENT r'''
@0:\"\"\"Returns a value\"\"\"
''';
</dd>

<dt file="a1.py">Disambiguate by setting the <update-target> to a specific <identifier_matcher></dt>
<dd>
-- Set the update target to "a". Notice "a_def1" is unambiguous inside "a"
-- Matches the function at any level of nesting *inside* the update target
UPDATE FUNCTION "a"
FROM FILE "a1.py"
INSERT INTO FUNCTION "a_def1" TOP
WITH CONTENT r'''
@0:\"\"\"Returns a value\"\"\"
''';
</dd>

<dt file="a2.py">Replace all occurrences of a string</dt>
<dd>Replace references to 'a1x' with 'a1' in all lines</dd>
<dd>
-- Replace ALL occurrences of 'a1x' with 'a1' using a simple CASE WHEN...THEN filter
UPDATE CLASS "A"
  FROM FILE "a2.py"
REPLACE WHOLE WITH CASE
  WHEN REGEX r'''a1x''' THEN SUB
    r'''a1x'''
    r'''a1'''
END;
</dd>
<dd>
-- Alternative form (more specific)
UPDATE CLASS "A"
  FROM FILE "a2.py"
REPLACE WHOLE WITH CASE
  WHEN REGEX r'''a1x''' THEN SUB
    r'''\\(a1x\\)'''
    r'''(a1)'''
END;
</dd>
<dd>Replace references to 'a2x' with 'a2' in all lines except comment lines</dd>
<dd>
-- To avoid touching the comment line, now we *MUST* be more specific in the SUB clause
UPDATE CLASS "A"
  FROM FILE "a2.py"
REPLACE WHOLE WITH CASE
  WHEN REGEX r'''a2x''' THEN SUB
    r'''\\(a2x\\)'''
    r'''(a2)'''
END;
</dd>
<dd>
-- Alternative form (directly skipping all comment lines)
UPDATE CLASS "A"
  FROM FILE "a2.py"
REPLACE WHOLE WITH CASE
  WHEN REGEX r'''^#''' THEN CONTINUE
  WHEN REGEX r'''a2x''' THEN SUB
    r'''a2x'''
    r'''a2'''
END;
</dd>

<dt file="a3.py">Replace all print statements with logging calls while preserving indentation</dt>
<dd>
-- Using CASE WHEN...THEN
UPDATE FUNCTION "my_func"
  FROM FILE "a3.py"
REPLACE BODY WITH CASE
  WHEN REGEX r'''print\\(''' THEN SUB
    r'''print\\((.*)\\)'''
    r'''logging.info(\\1)'''
END;
</dd>
<dd>
-- Using an ed script
UPDATE FUNCTION "my_func"
  FROM FILE "a3.py"
REPLACE BODY WITH ED r'''
g/print(/s/print(\\(.*\\))/logging.info\\1/g
''';
</dd>

<dt file="a3">Remove duplicate blank lines (collapse multiple empty lines into one)</dt>
<dd>
UPDATE METHOD "anotherFunction"
FROM FILE "a3.py"
REPLACE BODY WITH ED r'''
g/^$/,/[^$]/-j
''';
</dd>

<dt file="a3">Remove all comments</dt>
<dd>
UPDATE METHOD "anotherFunction"
FROM FILE "a3.py"
REPLACE BODY WITH ED r'''
g/^\\s*#/d
''';
</dd>

<dt file="a3">Add error handling around function calls</dt>
<dd>
UPDATE METHOD "anotherFunction"
FROM FILE "a3.py"
REPLACE BODY WITH ED r'''
's/^(\\s*)(.*\\(\\))/\\1try:\\
\\1    \\2\\
\\1except Exception as e:\\
\\1    logging.error(f"Failed: {e}")/g
''';
</dd>

<dt file="a3.py">Replace many occurrences of a word and also delete multiple lines</dt>
<dd>To replace `lops` with `loops` in many places, it's more concise to use a `WHEN..THEN` filter with a `REGEX` matcher</dd>
<dd>Let's also delete all lines containing the expression 'dummy...'</dd>
<dd>
UPDATE METHOD "anotherFunction"
  FROM FILE "a3.py"
REPLACE BODY
WITH CASE
  WHEN REGEX r'''dummy\\.\\.\\.''' THEN REMOVE
  WHEN REGEX r'''lops''' THEN SUB
    r'''lops'''
    r'''loops'''
END;
</dd>

<dt file="a3.py">Delete all empty lines in a method</dt>
<dd>
-- Using WHEN...THEN filter
UPDATE METHOD "anotherFunction"
FROM FILE "a3.py"
REPLACE BODY WITH CASE
  WHEN EMPTY THEN REMOVE
END;
</dd>
<dd>
-- Using an ed script filter
UPDATE METHOD "anotherFunction"
FROM FILE "file.py"
REPLACE BODY WITH ED r'''
g/^$/d
''';
</dd>

<dt file="a3.py">Refactor a method into a stand-alone, top level function</dt>
<dd>Let's choose method `myFirstFunction` for our example</dd>
<dd>
-- 1. Move the `myFirstFunction()` method from the `MyClass` class, placing it at the top level, just before the line where its class starts.
UPDATE FILE "a3.py"
MOVE METHOD "myFirstFunction"
INSERT BEFORE CLASS "MyClass"
  RELATIVE INDENTATION 0; -- the function being moved will start at the same indentation as the class `MyClass`

-- 2. Update the copied function to remove references to `self`, now declaring `instance_var_1` as parameter
UPDATE FUNCTION "myFirstFunction"
  FROM FILE "a3.py"
REPLACE WHOLE
WITH CASE
  WHEN REGEX r'''self,''' THEN SUBS 
    r'''self,'''
    r'''instance_var_1: str,'''
  WHEN REGEX r'''instance_var_1''' THEN SUBS
    r'''self\\.(instance_var_1)''' -- capture the part we want to keep
    r'''\\1''' -- replace the match with captured group 1
END;

-- 3. Update ALL call sites of the method `myFirstFunction` to call the new top-level function with the same name, passing `instance_var_1` as argument
UPDATE METHOD "anotherFunction"
  FROM FILE "a3.py"
REPLACE BODY WITH CASE
  WHEN REGEX r'''self\\.myFirstFunction''' THEN SUBS
    r'''self\\.(myFirstFunction\\()''' -- capture the part we want to keep (which includes the opening paranthesis)
    r'''\\1instance_var_1, ''' -- \\1 also contains the '(' so we immediately write 'instance_var_1, '
END;
</dd>

</dl>

"""

    #  TODO

    # To replace 'failUnlessEqual' with 'assertEqual' using Comby notation:
    # ```CEDARScript
    # UPDATE PROJECT
    # REAFCTOR LANGUAGE "comby"
    # WITH PATTERN '''
    # comby 'failUnlessEqual(:[a],:[b])' 'assertEqual(:[a],:[b])' example.py
    # '''
    # ```

    #   + When presented with a code change task:
    #  +
    #  + 1. Analysis Phase:
    #  +    a. Carefully read and understand the requested changes
    #  +    b. Identify which files need to be modified
    #  +    c. If files aren't in chat yet:
    #  +       - List ONLY files that need changes (not context files)
    #  +       - Wait for user to add them
    #  +       - Don't proceed until files are added
    #  +
    #  + 2. Planning Phase:
    #  +    a. Break down the changes into logical steps
    #  +    b. For each step, determine:
    #  +       - Which file(s) to modify
    #  +       - Which CEDARScript commands to use
    #  +       - What order to apply changes
    #  +    c. Look for ways to make commands more concise:
    #  +       - Can multiple changes be combined?
    #  +       - Is there a shorter way to express the change?
    #  +       - Are all lines in the command necessary?
    #  +
    #  + 3. Implementation Phase:
    #  +    Write the CEDARScript commands:
    #  +    a. Start with a brief explanation of the changes
    #  +    b. Write the commands in order of application
    #  +    c. Use comments to explain complex changes
    #  +    d. Format properly:
    #  +       ```CEDARScript
    #  +       -- Step 1: Brief description
    #  +       UPDATE ...;
    #  +
    #  +       -- Step 2: Brief description
    #  +       UPDATE ...;
    #  +       ```
    #  +
    #  + 4. Error Recovery Phase:
    #  +    If a command fails:
    #  +    a. Analyze error details in <error-details> tag
    #  +    b. Identify the specific issue
    #  +    c. Consider alternatives:
    #  +       - Different command structure?
    #  +       - Different reference points?
    #  +       - Different approach entirely?
    #  +    d. Apply fix and retry
    #  +
    #  + Remember:
    #  + - Commands are applied in order
    #  + - Each command sees results of previous commands
    #  + - Don't retry successful commands
    #  + - Keep commands as concise as possible
    #  + </li>


    # Appears twice (as SYSTEM and as USER):
    system_reminder = """When presented with a code change task:
<action>
<step>Identify the files to be updated</step>
<step>Determine the best, concise sequence of targeted CEDARScript commands to express the code change in shortest possible way.
Super careful to avoid syntax errors.</step>
<step>If your script fails, carefully analyze the error details inside tag <error-details> and tell me how you can overcome the problem, then try harder to get it right.
</step>
</action>

- Pay attention to which filenames the user wants you to edit, especially if they are asking you to create a new file;
- Use the exact file path for the file that needs to be changed (remember you can only change files that the user added to the chat!);
- Each CEDARScript command is applied in the same order as they appear. If a command fails to be applied, all commands before it were correctly applied (don't retry those!). Once a command is applied on a file, the next command will see
the update version of that file, with all changes that were applied by earlier commands; - It's crucial to strive to provide *as concise and small as possible*, targeted CEDARScript commands that each change a given aspect of the program, so that humans can easily understand what's changing;
- Try *HARD* to minimize the number of unchanged lines in a CEDARScript command and to have a very *concise* script;
- To move code within a file or identifier (class, method or function), you *MUST* use the `UPDATE ... MOVE ...` construct to minimize script size (DON'T use `WITH CONTENT`);
<IMPORTANT>
1. You wmust try the alternative form `UPDATE CLASS..MOVE FUNCTION` (instead of `UPDATE FUNCTION..MOVE WHOLE`) if the latter fails
2. If there are MULTIPLE identifiers with the same name, you *MUST* choose an appropriate reference that is unambiguous! 
</IMPORTANT>
<p>Selecting Reference Points for Code Locations:
When choosing lines/elements to reference in commands:
1. Uniqueness Rule: *NEVER* reference an ambiguous line/identifier (that is, appearing multiple times);
Check if your chosen reference appears multiple times in the file.
To disambiguate a line:
  - Find a unique alternative nearby (preferred).
  - Use a *context-relative line number*
To disambiguate an identifier:
  - Use the *parent chain*: prepend one or more parent names to the identifier name, as in `MyClass.MyOtherClass.my_method`
</p>

<dl>Avoiding Common Mistakes</dl>

<dt>Reference selection</dt>
<dd>
Never use ambiguous references. When selecting reference points, follow this priority:
1. For identifiers, use parent chains: "MyClass.my_method"
2. For lines, prefer REGEX line matchers (if that fails, try PREFIX)
3. Use OFFSET 0 for first match
</dd>

<dt>context-relative-line-numbers</dt>
<dd>
- Incorrect: Start counting at the function/method's body
- Correct: Start counting at the first line where the function/method's signature appears.
</dd>

<dt>content_literal: relative-indent-level</dt>
<dd>
Incorrect: Using `REPLACE LINE` and providing <content_literal> a non-zero <relative-indent-level>
Correct: When using `REPLACE LINE`, remember that the *horizontal positioning reference point* is the LINE iteself, so we need to use 0 as the <relative-indent-level> so that the line keeps its original indent level.
</dd>

<dt>Turning method into top-level function</dt>
<dd type="*CRUCIAL*">
After moving the method to the top level (thus turning it into a function), you *MUST*:
1. Update the new function to remove ALL references to `self` (i.e. in its function signature and its body)
2. Update ALL call sites of the moved method throughout the file to remove the `self.` prefix
</dd>


<dt>FROM keyword ordering</dt>
<dd>FROM keyword must directly be followed by keyword `FILE` or `PROJECT`, never by `CLASS`, `FUNCTION` or other keywords</dd>
<dd>
1) Incorrect: `FROM` followed by `CLASS`, as in `UPDATE FILE "file.py" REPLACE FUNCTION "__init__" FROM CLASS "A"`
   - Correct  : `FROM` keyword followed by `FILE` or `PROJECT`, as in `UPDATE CLASS "A" FROM FILE "file.py" REPLACE FUNCTION "__init__"`
2) Incorrect: `DELETE METHOD "MyClass.something" FROM FILE "my_file.py"`
   - Correct (best): `UPDATE FILE "my_file.py" DELETE METHOD "MyClass.something";`
   - Also correct  : `UPDATE CLASS "MyClass" FROM FILE "my_file.py" DELETE METHOD "something";`
</dd>

<dt>Clause Ordering</dt>
<dd>`FROM` clause *must* come *before* an *action* clause like `DELETE`, `MOVE`, `INSERT`, `REPLACE`</dd>
<dd>
- Incorrect: UPDATE, REPLACE, FROM, as in `UPDATE FILE "file.py" REPLACE FUNCTION "__init__" FROM CLASS "A"`
- Correct  : UPDATE, FROM, REPLACE, as in `UPDATE CLASS "A" FROM FILE "file.py" REPLACE FUNCTION "__init__"`
</dd>

<dt>Action clause without main clause</dt>
<dd>Any *action* clause like `DELETE`, `MOVE`, `INSERT` etc *MUST* be preceded by its main clause (`UPDATE`)</dd>
<dd>
- Incorrect: `UPDATE FILE "file.py" DELETE LINE "print(a)"; DELETE LINE "print(b)";`
- Correct: `UPDATE FILE "file.py" DELETE LINE "print(a)"; UPDATE FILE "file.py" DELETE LINE "print(b)";`
</dd>

<dt>Triple Backtick</dt>
<dd>When using *triple backticks*, you *MUST* pair *every single backtick* with a preeding backslash (total of 3 pairs of backslash-backtick)</dd>
<dd>
- Incorrect (*without* a preceding \\ for each backtick): `WITH CONTENT r'''@0:Bash: ``` rm *.py ```''';`
- Correct (*every* single backtick is preceded by a "\\"): `WITH CONTENT r'''@0:Bash: \\`\\`\\` rm *.py \\`\\`\\`''';`
</dd>

<dt>Using parenthesis inside <repl></dt>
<dd>NEVER escape parentheses inside <repl>!
- Incorrect:  r'''def a_method\\(params\\)'''
- Correct  :  r'''def a_method(params)'''
</dd>

</dl>

{lazy_prompt}
ONLY EVER RETURN CODE IN *CEDARScript block*!
CEDARScript commands MUST BE *AS CONCISE AS POSSIBLE*!
ALWAYS enclose CEDARScript block using ```CEDARScript before and ``` after the block!
You MUST write <NOCEDARSCRIPT/> as the last line if:
1) You just want *show* some CEDARScript commands to the user instead of executing them;
2) If there are no CEDARScript blocks to execute.
{shell_cmd_reminder}
"""
    # TODO Finally, rephrase and summarize my instructions. Only then, respond. Do so by thinking step by step.

    example_messages = CEDARScriptPromptsBase.example_messages + [
        dict(
            role="user",
            content="""
```file.py
class MyClass(NamedTuple):
    instance_var_1: str = '4r3'
    def myFirstFunction(self, name: str, age: int):
        \"\"\"Lorem ipsum dolor sit amet
        Args:
            name: name
            age: age
        \"\"\"
        if age > 50
          return a + 5 + 7 + 9
        if age > 70
          a = doSomething(name, age)
          return a + 5 + 1 + len(self.instance_var_1) * 7
      def middle(self):
          pass
      def anotherFunction(self, name: str, age: int):
          # Check and store in 'b' and 'bb'
          # Remember NOT to call self.myFirstFunction(a, b) ever !!!
          b = checkVal(45, "strict", self.myFirstFunction(name, age), 8, "tops")
          ba = 4 + checkVal(77, "strict", "z" + self.myFirstFunction("x" + name, 4 + age), 8, "tops")
          bb = checkVal(7, "lax", self.myFirstFunction(name, age), 2, "bottom")
          c = checkVal(4, "strict", self.myFirstFunction("x", 4), 8, "tops")
          return b + bb
```
  Refactor method myFirstFunction to be a stand alone, top level function.
              """
        ),
        dict(
            role="assistant",
            content="""Here's my plan to make this refactoring:
1. Move the `myFirstFunction()` method from the `MyClass` class, placing it at the top level, just before the line where its class starts;
2. Update the copied function to remove references to `self` and declare any required instance members as function parameters;
3. Update call sites of the method `myFirstFunction` to call the new top-level function with the same name, passing any instance members as arguments;

Here's the CEDARScript script:

{fence[0]}CEDARScript
-- 1. Move the `myFirstFunction` method from the `MyClass` class, placing it at the top level, just before the line where its class starts.
UPDATE METHOD "MyClass.myFirstFunction"
  FROM FILE "file.py"
MOVE WHOLE
INSERT BEFORE CLASS "MyClass"
  RELATIVE INDENTATION 0; -- the block of code being moved wil start at the same indentation as the 'reference mark'

-- 2. Update the copied function to remove references to `self`, now declaring `instance_var_1` as parameter
/* Match the line with the prefix that contains the OLD version of the line (`def myFirstFunction(self,`) and
replaces the whole line with the NEW version we desire: `def myFirstFunction(instance_var_1: str,`
*/
UPDATE FUNCTION "myFirstFunction"
  FROM FILE "file.py"
REPLACE WHOLE WITH CASE
  WHEN REGEX r'''def myFirstFunction''' THEN SUB
    r'''def myFirstFunction\\(self, name: str, age: int\\):'''
    r'''def myFirstFunction(instance_var_1: str, name: str, age: int):'''
  WHEN REGEX r'''self\\.instance_var_1''' THEN SUB
    r'''self\\.(instance_var_1)''' -- capture the part we want to keep, leaving out the part to remove
    r'''\\1''' -- replace the match with the part we captured in group 1
END;

-- 3. Update ALL call sites of the method `myFirstFunction` to call the new top-level function with the same name, passing `instance_var_1` as argument
-- Make sure to search for the OLD content and replace it with the NEW content we want
UPDATE METHOD "MyClass.anotherFunction"
  FROM FILE "file.py"
REPLACE BODY WITH CASE
  WHEN LINE PREFIX '''#''' THEN CONTINUE
  WHEN REGEX r'''self\\.myFirstFunction\\(''' THEN SUB
    r'''self\\.(myFirstFunction\\()''' -- capture the part we need to keep
    r'''\\1''' -- replace the match with the part we need to keep (was captured in group 1)
END;
{fence[1]}
""",
        ),
        dict(
            role="user",
            content="""
```file.py
class GreeterClone:
    def __init__(self):
        pass
    def print_greeting_number(self):
        pass
    def print_with_prefix(self, prefix: str, name: str):
        pass
    def greet(self, name):
        pass
class Greeter:
    def __init__(self):
        pass
    def print_greeting_number(self):
        pass
    def print_with_prefix(self, prefix: str, name: str):
        pass
    def greet(self, name):
        print('...Nice to meet you!')
        print("Hope you're doing well!")
```

In `Greeter` class above, we have placeholder methods that need to be implemented, and the last method should:
1. Print the name using prefix `Hi, ` before it does anything else (should be the very first thing);
2. Print how many greetings have been printed so far as the last thing.
"""
        ),
        dict(
            role="assistant",
            content="""Here's my plan to implement the requested changes:
1. Add instance variable `greeting_count: int` to the `Greeter` class to keep track of the greeting count;
2. Implement the `print_with_prefix()` method to print parameter `name` prefixed with the `prefix` parameter;
3. Insert a call to the `print_with_prefix()` method at the top of the last method (`greet()`);
4. Insert code at the bottom of the `greet()` method to print the greeting count and increment it.

Here's the CEDARScript script:

{fence[0]}CEDARScript
-- 1. Add instance variable `greeting_count: int` to the `Greeter` class to keep track of the greeting count
-- As method `__init__` exists in more than 1 class, use `parent chain` to disambiguate
UPDATE METHOD "Greeter.__init__"
  FROM FILE "file.py"
REPLACE BODY
WITH CONTENT r'''
@0:self.greeting_count: int = 0
''';

-- 2. Implement the `print_with_prefix()` method to print parameter `name` prefixed with the `prefix` parameter;
-- As method `print_with_prefix` exists in more than 1 class, we specify which one we want to reference
UPDATE METHOD "Greeter.print_with_prefix"
  FROM FILE "file.py"
REPLACE BODY
WITH CONTENT r'''
@0:print(f"{{prefix}}{{name}}")
''';

-- 3. Insert a call to the `print_with_prefix()` method at the top of the last method (`greet`);
-- As method `greet` exists in more than 1 class, we specify which one we want to reference
UPDATE CLASS "Greeter"
  FROM FILE "file.py"
INSERT INTO METHOD "greet" TOP -- at the TOP of the function body
-- The function body is the reference indent level; `@0:` means to use that same level 
WITH CONTENT r'''
@0:print_with_prefix('Hi, ', name)
''';

-- 4. Insert code at the bottom of the body of `greet()` method to increment the greeting count and print it.
-- As method `greet` exists in more than 1 class, we specify which one we want to reference
UPDATE CLASS "Greeter"
  FROM FILE "file.py"
INSERT INTO METHOD "greet" BOTTOM
-- The function body is the reference indent level; `@0:` means to use that same level 
WITH CONTENT r'''
@0:self.greeting_count += 1
@0:print(f'There have been {{self.greeting_count}} greetings so far.')
''';
{fence[1]}

Notes to self:
1. As the code to be changed was provided in the message, we're using file name "file.py".
2. When using `INTO`, the body of the function or class is implicit, so we can NEVER write `BODY` after `INTO`.
""",
        ),
        dict(
            role="user",
            content="""```file.py
class A0:
    def __init__(self, v: int):
        self.instance_var = v
    def calc1(self, a):
        return a * self.instance_var
    def calc2(self, a):
        # Call calc1...
        c = self.calc1(5)
class A:
    def __init__(self, v: int):
        self.instance_var = v
    def calc1(self, a):
        \"\"\"
        'calc1' is a method
        that takes 'a' as parameter.
        and then
        perform a calculation
        that multiplies 'a' (the first argument
        after 'self') by a value stored in 'self.instance_var'.
        \"\"\"
        # Some more comments...
        return a * self.instance_var
    def calc2(self, a):
        # c is declared
        c = 4
        # print
        print(c)
        # Call calc1...
        c = self.calc1(
            2
        )
        # print
        print(c)
        # inc c
        c += 1
        # print
        print(c)
```
Refactor the `calc1` method in the `A` class to be a stand alone, top level function.
"""
        ),
        dict(
            role="assistant",
            content="""Here's my plan to implement the requested changes:
1. Move the `calc1()` method from the `A` class, placing it at the top level, just before the line where its class starts;
2. Update the copied function to remove references to `self`, now declaring `instance_var` as parameter;
3. Update ALL call sites of the method `calc1()` to call the new top-level function with the same name, passing `instance_var` as argument;

Here's the CEDARScript script:

{fence[0]}CEDARScript
-- 1. Move the `calc1` method from the `A` class, placing it at the top level, just before the line where its class starts
-- As method `calc1` exists in more than 1 class, we specify which one we want to reference
UPDATE METHOD "A.calc1"
  FROM FILE "file.py"
MOVE WHOLE
INSERT BEFORE CLASS "A"
  RELATIVE INDENTATION 0;

-- 2. Update the copied function to remove references to `self`, now declaring `instance_var` as parameter
-- Make sure to search for the OLD content and replace it with the NEW content we want
UPDATE FUNCTION ".calc1"
  FROM FILE "file.py"
REPLACE WHOLE WITH CASE
  WHEN REGEX r'''def calc1''' THEN SUB
    r'''def calc1\\(self, a\\):'''
    r'''def calc1(instance_var: int, a):'''
  WHEN REGEX r'''self\\.instance_var''' THEN SUB
    r'''self\\.(instance_var)''' -- match and capture the part of the old code we need to keep
    r'''\\1''' -- replace the match with the part we need to keep (was captured in group 1)
END;

-- 3. Update ALL call sites of the method `calc1` to call the new top-level function with the same name, passing `instance_var` as argument
UPDATE METHOD "A.calc2"
  FROM FILE "file.py"
REPLACE BODY WITH CASE
  WHEN REGEX r'''self\\.calc1\\(''' THEN SUB
    r'''(self\\.)(calc1\\()'''
    r'''\\2\\1instance_var, '''
END;
{fence[1]}""",
        ),
        dict(
            role="user",
            content="""```file.py
class A0:
    def __init__(self, v: int):
        self.instance_var = v
    def calc1(self, a):
        return a * self.instance_var
    def calc2(self, a):
        # Call calc1...
        # I'm a bad line, get rid of me!
        c = self.calc1(5)
class A:
    def __init__(self, v: int):
        self.instance_var = v
    def calc1(self, a):
        return a * self.instance_var
    def calc2(self, a):
        # print a
        # I'm a bad line, get rid of me!
        print(a)
        # Call calc1...
        c = ["x", str(self.calc1(
            5), "xx"]
        c = ["x", str(self.calc1(
            6), "xx"]
        # Done...
        return c
```
Refactor the `calc1` method in the `A` class to be a stand alone, top level function. Also, there's some 'bad' lines that clearly need to be removed.
"""
        ),
        dict(
            role="assistant",
            content="""Here's my plan to implement the requested changes:
1. Move the `calc1()` method from the `A` class, placing it at the top level, just before the line where its class starts;
2. Update the copied function to remove references to `self`, now declaring `instance_var` as parameter;
3. Update ALL call sites of the method `calc1()` to call the new top-level function with the same name, passing `instance_var` as argument;
4. Delete the bad line;

Here's the CEDARScript script:

{fence[0]}CEDARScript
-- 1. Move the `calc1` method from the `A` class, placing it at the top level, just before the line where its class starts
-- As method `calc1` exists in more than 1 class, we specify which one we want to reference
UPDATE METHOD "A.calc1"
  FROM FILE "file.py"
MOVE WHOLE
INSERT BEFORE CLASS "A"
  RELATIVE INDENTATION 0;

-- 2. Replace the whole copied function to remove references to `self` and declare `instance_var` as parameter
-- Now, `calc1` exists as a top-level function before class `A`
-- It's better to replace the whole function because the function is small
UPDATE FUNCTION ".calc1" OFFSET 1
  FROM FILE "file.py"
REPLACE WHOLE
WITH CONTENT r'''
@0:def calc1(instance_var: int, a):
@1:return a * instance_var
''';

-- 3. Update ALL call sites of the method `calc1` to call the new top-level function with the same name, passing `instance_var` as argument
UPDATE FUNCTION "A.calc2"
  FROM FILE "file.py"
REPLACE BODY WITH CASE
  WHEN REGEX r'''^# I'm a bad''' THEN REMOVE
  WHEN REGEX r'''self\\.calc1\\(''' THEN SUB
    r'''(self\\.)(calc1\\()'''
    r'''\\2\\1instance_var, '''
END;

-- 4. Delete the single remaining bad line (it's in the other method)
UPDATE FILE "file.py"
DELETE LINE REGEX r'''^# I'm a bad'''; -- Removes the whole line that starts with that prefix
{fence[1]}""",
        ),
        dict(
            role="user",
            content="""```file.py
def calc1(a):
    return a * 7.0
def calc2(a):
    c = ["x", str(calc1(
        5), "xx")]
    c = ["x", str(calc1(
        6), "xx")]
    # Done...
    return c
```
Refactor the calc1 function to introduce tax: float as first parameter.
The function should use the new parameter instead of 7.
Function calc2 should also get this new parameter, but as last parameter and with name base_tax and default value 1.3.
"""
        ),
        dict(
            role="assistant",
            content="""Here's my plan to implement the requested changes:
1. Update the function signature of `calc1()` to add parameter `tax: float` as the first one and use the new parameter instead of `7`;
2. Update the function signature of `calc2()` to add parameter `base_tax: float = 1.3` as the last one;
3. Update ALL call sites of `calc1()` to pass `base_tax` as the first argument;

Here's the CEDARScript script:

{fence[0]}CEDARScript
-- 1. Update the function signature of `calc1()` to add parameter `tax: float` as the first one and use the new parameter instead of `7`
UPDATE FUNCTION "calc1"
  FROM FILE "file.py"
REPLACE WHOLE
WITH CONTENT '''
@0:def calc1(tax: float, a):
@1:return a * tax
''';

-- 2. Update the function signature of `calc2()` to add parameter `base_tax: float = 1.3` as the last one
-- 3. Update ALL call sites of `calc1()` to pass `base_tax` as the first argument
UPDATE FUNCTION "calc2"
  FROM FILE "file.py"
REPLACE WHOLE WITH CASE
  WHEN REGEX r'''def calc2\\(''' THEN SUBS
    r'''def calc2\\(a\\):'''
    r'''def calc2(a, base_tax: float = 1.3):'''
  WHEN REGEX r'''calc1\\(''' THEN SUB
    r'''calc1\\('''
    r'''calc1(base_tax, '''
END;
{fence[1]}""",
        ),
        dict(
            role="user",
            content="""```file.py
class A:
    def _calc(self, a):
        return a
    def _check(self, a: int, b, c):
        if a > 0:
            return self._calc(
                "a thing or two"
            )
        else:
            return list(
                self._calc(
                    my_list.include(self._candidate(
                        a, "string 1", 4
                    ))
                    for index, item in enumerate(a.the_elements)
                )
            )

    def _candidate(self, existing_params):
        return a
```
Refactor the `_candidate` method to be a stand alone, top level function.
"""
        ),
        dict(
            role="assistant",
            content="""Here's my plan to implement the requested changes:
1. Move the `_candidate()` method from the `A` class, placing it at the top level, just before the line where its class starts;
2. Update the copied function to remove references to `self`;
3. Update ALL call sites of the method `_candidate()` to call the new top-level function with the same name;

Here's the CEDARScript script:

{fence[0]}CEDARScript
-- 1. Move the `_candidate()` method from the `A` class, placing it at the top level, just before the line where its class starts
UPDATE METHOD "_candidate"
  FROM FILE "file.py"
MOVE WHOLE
INSERT BEFORE CLASS "A"
  RELATIVE INDENTATION 0;

-- 2. Update the copied function to remove references to `self`
UPDATE FUNCTION "_candidate"
  FROM FILE "file.py"
REPLACE WHOLE WITH CASE
  WHEN REGEX r'''def _candidate\\(''' THEN SUB
    r'''def _candidate\\(self, existing_params\\):'''
    r'''def _candidate(existing_params):'''
END;

-- 3. Update ALL call sites of the method `_candidate()` to call the new top-level function with the same name
UPDATE METHOD "_check"
  FROM FILE "file.py"
REPLACE WHOLE WITH CASE
  WHEN REGEX r'''self\\._candidate\\(''' THEN SUB
    r'''self\\.(_candidate\\()'''
    r'''\\1'''
END;
{fence[1]}""",
        ),
        dict(
            role="user",
            content="""```file.py
class A:
    def _calc(self, a):
        return a
    def _check(self, a: int, b, c):
        if a > 0:
            return self._candidate( "a thing or two"
            )
        else:
            return list(
                self._calc(
                    my_list.include(self._candidate(
                        a, "string 1", 4
                    )))
                    for index, item in enumerate(a.the_elements)
                )
            )

    def _candidate(self, existing_params):
        return a
```
Refactor the `_candidate` method to be a stand alone, top level function.
"""
        ),
        dict(
            role="assistant",
            content="""Here's my plan to implement the requested changes:
1. Move the `_candidate()` method from the `A` class, placing it at the top level, just before the line where its class starts;
2. Update the copied function to remove references to `self`;
3. Update ALL call sites of the method `_candidate()` to call the new top-level function with the same name;

Here's the CEDARScript script:

{fence[0]}CEDARScript
-- 1. Move the `_candidate()` method from the `A` class, placing it at the top level, just before the line where its class starts
-- As method `_candidate` only exists in one place, it's unambiguous, but this time we wmust try the alternative form `UPDATE CLASS..MOVE FUNCTION` (instead of `UPDATE FUNCTION..MOVE WHOLE`) because the latter failed last time we tried.
UPDATE CLASS "A"
  FROM FILE "file.py"
MOVE METHOD "_candidate"
INSERT BEFORE CLASS "A"
  RELATIVE INDENTATION 0;

-- 2. Update the copied function to remove references to `self`
UPDATE FUNCTION "_candidate"
  FROM FILE "file.py"
REPLACE WHOLE WITH CASE
  WHEN REGEX r'''def _candidate\\(''' THEN SUB
    r'''def _candidate\\(self, existing_params\\):'''
    r'''def _candidate(existing_params):'''
END;

-- 3. Update ALL call sites of the method `_candidate()` to call the new top-level function with the same name
-- There are two or more of this line prefix 'self._candidate'
UPDATE METHOD "A._check"
  FROM FILE "file.py"
REPLACE BODY WITH CASE
  WHEN REGEX r'''self\\._candidate\\(''' THEN SUB
    r'''self\\.(_candidate\\()'''
    r'''\\1'''
END;
{fence[1]}""",
        ),
    ]
