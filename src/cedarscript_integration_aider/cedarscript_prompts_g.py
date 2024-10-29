# flake8: noqa: E501

from .cedarscript_prompts_base import CEDARScriptPromptsBase


class CEDARScriptPromptsGrammar(CEDARScriptPromptsBase):

    def edit_format_name(self):
        return f"{super().edit_format_name()}-g"

    final_remarks = CEDARScriptPromptsBase.final_remarks_brain

    edit_format_training = """## CEDARScript Quick Reference Guide
It's a *SQL-like* language used to express code manipulations (via DDL and DML Write commands) and to help an LLM examine and understand the codebase (via DML Read-Only command).
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

<dt>update-target: [<identifierMarker> FROM] FILE "<path>"</dt>
<dd>Specifies what to update:
- Direct file update (FILE "path"); Sets *reference point* for *vertical positioning* to the first line in the file.
- A specific <identifierMarker> FROM FILE "path"; Sets *reference point* for *vertical positioning* to the \
first line where the identifier is declared (function signature, etc)
</dd>
<dd>Sets *reference point* for *vertical positioning* (Context-Relative Line Numbers)</dd>

<dt>update-action: (<action-mos> | <action-region>)</dt>
<dd>Possible actions: DELETE | MOVE | INSERT | REPLACE</dd>
<dd>Sets *reference point* for *horizontal positioning* (Relative Indent Level)</dd>
<dd>The reference point is the term chosen for the (MOVE|INSERT|REPLACE) action</dd>

<dt>contents: (<content_literal> | <content_from_segment>)</dt>
<dd>Optional specification of new content:
- content_literal: direct text using <relative-indent-level-string>
- content_from_segment: content taken from existing code
</dd>

<dt>action-mos   : ( <update_delete_region_clause> | MOVE <marker_or_segment> <update_move_clause_destination> | <insert_clause> | <replace_region_clause> )</dt>
<dd>Use when update-target is a FILE</dd>
<dt>action-region: ( <update_delete_region_clause> | MOVE <region_field>      <update_move_clause_destination> | <insert_clause> | <replace_region_clause> )</dt>
<dd>Use when update-target is an <identifierMarker></dd>

</dl>
</syntax-high-level>

<syntax-detailed>
<dl>

# 3 forms are valid:

1. <dt>UPDATE FILE "<path>" <action-mos> [WITH <contents>]</dt>
<dd>Sets *reference point* for *vertical positioning* to the first line in the file</dd>

2. <dt>UPDATE <identifierMarker> FROM FILE "<path>" <action-region> [WITH <contents>]</dt>
<dd>Sets *reference point* for *vertical positioning* to the first line where the identifier is declared \
(function signature, etc)</dd>

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
<dt>marker: (<lineMarker> | <identifierMarker>)</dt>
<dd></dd>
<dt>lineMarker: LINE ('''<string>''' | <context-relative-line-number> | REGEX r"<regex>" | PREFIX '''<string>''' | SUFFIX '''<string>''') [OFFSET <offset>]</dt>
<dd>Points to specific line via:
- its *contents*, if it's unambiguous (don't use line content if the line appears multiple times);
- its *context-relative line number* (Must use this if other types failed;
- a regular expression pattern (REGEX);
- a string that matches from start of line (PREFIX);
- a string that matches from end of line (SUFFIX);
</dd>
<dt>identifierMarker: (VARIABLE | FUNCTION | METHOD | CLASS) "[parent-chain.]<name>" [OFFSET <offset>]</dt>
<dd>Name of an identifier</dd>
<dd>If there are 2 or more with same name, prefixed it with its *parent chain* (names of its parents separated by a dot) to disambiguate it.
Another way to disambiguate is to use `OFFSET <n>` to pinpoint one.
</dd>
<dt>parent-chain: string</dt>
<dd>A *parent chain* is a dot-separated list of parents of <identifier> to help disambiguate it</dd>
<dd>When a reference is ambiguous (multiple matches exist for it), it must be disambiguated. Parent chains are a way to do that</dd>
<dd>Examples:
- "name" (no parent chain, matches at any nesting level, including at the top level)
- ".name" (only root in the chain, only matches "name" if it's at the top level of the file)
- "C.name" (1 parent in the chain, matches "name" as long as "C" is a direct parent of it)
- "B.C.name" (2 parents in the chain, requires "B" to be a direct parent of "C", and "C" a direct parent of "name")
- ...
</dd>
<dt>offset: integer</dt>
<dd>Determines how many matches to skip</dd>
<dd>When a reference is ambiguous (multiple matches exist for it), it must be disambiguated. Setting an OFFSET is a way to do that</dd>
<dd>Examples:
OFFSET 0: skips 0 items (so, points to the *1st* match);
OFFSET 1: skips 1 matches, so points to the *2nd* match;
OFFSET 2: skips 2 matches, so points to the *3rd* match;
OFFSET n: skips n matches, thus specifies the (n+1)-th match;
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
<dt>relpos_into: INTO <identifierMarker> (TOP | BOTTOM)</dt>
<dd>Points to inside `identifierMarker` (either the body's TOP or BOTTOM region). The *horizontal reference point* is the body</dd>
<dd>Use cases: When inserting content (e.g. a docstring or a return statement) either at the TOP or BOTTOM of a function or class body</dd>
<dt>relpos_bai: (<relpos_beforeafter> | <relpos_into>)</dt>
<dd></dd>
<dt>relative_indentation: RELATIVE INDENTATION <relative-indent-level></dt>
<dd>The reference point for the horizontal positioning of <relative_indentation> is the <marker> in (<insert_clause> | <replace_region_clause>)</dd>

## Content Sources
<dt>content_literal: CONTENT '''<relative-indent-level-string>'''</dt>
<dd>Examples:</dd>
<dd>CONTENT '''@0:return "x"'''</dd>
<dd>CONTENT '''@-1:if a > 0:'''</dd>
<dd>CONTENT '''
@0:return "x"
@-1:if a > 0:
@0:b += 1
'''</d>
<dd>CONTENT \"\"\"
@0:my_multiline_text = '''test
@1:multi
@1:line
@0'''
\"\"\"</dd>
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
<dt>content_from_segment: [singlefile_clause] <marker_or_segment> [relative_indentation]</dt>
<dd></dd>
<dt>update_move_clause_destination: [TO FILE "<path>"] <insert_clause> [relative_indentation]</dt>

## Horizontal Positioning: Relative Indent Level

<dt>relative-indent-level-string: <relative-indent-prefix><line-1><newline>[<relative-indent-prefix><line-2><newline>]...</dt>
<dd>(... denotes repetition)</dd>
<dd>line-1, line-2 ... line-n is the actual content for each line</dd>
<dd>MUST be used when providing CONTENT blocks. Simplifies matching indentation with the existing code being changed</dd>
<dd>The CEDARScript runtime will handle the actual formatting and indentation in the target code file</dd>
<dt>relative-indent-prefix: @<relative-indent-level>:</dt>
<dt>relative-indent-level: integer</dt>
<dd>Determines *horizontal positioning* as a *relative* indent *level* compared to the *horizontal positioning reference point* \
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
<dd>NOTE: If you get `E999 IndentationError` message or any other indentation error, check that your relative indent levels \
follow these rules</dd>

## Vertical Positioning: Context-Relative Line Numbers
<dt>context-relative-line-number: integer</dt>
<dd>Determines *vertical positioning*. Represents the relative line number compared to the *vertical positioning reference point* \
(the reference point is the target chosen for the <update-target> - either the file itself or a specific <identifierMarker> in it)</dd>
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

## Explainers
TODO

## Cookbook
TODO

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

# When using REPLACE LINE n, there are TWO different reference points:
#
# 1 For line numbering: The method/function/class being referenced (in this case, method decode) is used to determine which line we're replacing
# 2 For relative indentation (@N:): The line being replaced (line 2) is the reference point for indentation
#
# <relative-indent-reference-points>
# # Reference point for relative indentation (@N:) depends on the command type:
#
# 1. For `REPLACE LINE n`:
# - Reference is the line being replaced (NOT the identifier containing it)
# - Example: If replacing line 2 of method foo(), and that line is indented 2 levels,
# use @0: to keep same level as that line
#
# 2. For `INTO (FUNCTION|METHOD|CLASS) ... (TOP|BOTTOM)`:
# - Reference is the body of the identifier
# - Example: If inserting at TOP of method body that's indented 1 level,
# use @0: to match body's indent level
#
# 3. For `(BEFORE|AFTER) (LINE|FUNCTION|METHOD|CLASS)`:
# - Reference is the item itself (not one line before/after)
# - Example: If inserting after a method definition indented 1 level,
# use @0: to match that method's indent level
#
# 4. For `REPLACE (FUNCTION|METHOD|CLASS)`:
# - Reference is where the identifier's definition starts
# - Example: If replacing a method indented 1 level,
# use @0: to match method's indent level, @1: for its body
# </relative-indent-reference-points>


# Appears twice (as SYSTEM and as USER):
    system_reminder = """When presented with a code change task:
<action>
<step>Identify the files to be updated</step>
<step>Determine the best, concise sequence of targeted CEDARScript commands to express the code change in shortest possible way.
Super careful to avoid syntax errors.</step>
<step>If your script fails, carefully analyze the error details inside tag <error-details> and tell me how you can overcome the problem, then try harder to get it right.
</step>
</action>
<important>
<ul>
<li>Pay attention to which filenames the user wants you to edit, especially if they are asking you to create a new file</li>
<li>Use the exact file path for the file that needs to be changed (remember you can only change files that the user added to the chat!)</li>
<li>Even when being concise, don't use `/dev/stdin` unless user provided a literal source code block directly in message</li>
<li>Each CEDARScript command is applied in the same order as they appear. If a command fails to be applied, all commands \
before it were correctly applied (don't retry those!). Once a command is applied on a file, the next command will see \
the update version of that file, with all changes that were applied by earlier commands.</li>
<li>It's crucial to strive to provide *as concise and small as possible*, targeted CEDARScript commands that each \
change a given aspect of the program, so that humans can easily understand what's changing</li>
<li>Try *HARD* to minimize the number of unchanged lines in a CEDARScript command and to have a very *concise* script</li>
<li>To move code within a file or identifier (class, method or function), you *MUST* use the `UPDATE ... MOVE ...` construct \
to minimize script size (DON'T use `WITH CONTENT`)
<IMPORTANT>
1. You wmust try the alternative form `UPDATE CLASS..MOVE FUNCTION` (instead of `UPDATE FUNCTION..MOVE WHOLE`) if the latter fails
2. If there are MULTIPLE identifiers with the same name, you *MUST* choose an appropriate reference that is unambiguous! 
</IMPORTANT>
</li>
<li>For `CONTENT` blocks, ALWAYS use `relative indent prefix` (which is the @N: part) for each line, where N is RELATIVE \
to the reference point specified in the `DELETE|MOVE|INSERT|REPLACE` clause (*not* the `identifier_from_file` clause).
The actual indentation characters (spaces or tabs) will be applied by the CEDARScript engine.
</li>
<li>Selecting Reference Points for Code Locations:
When choosing lines/elements to reference in commands:
1. Uniqueness Rule: *NEVER* reference an ambiguous line/identifier (that is, appearing multiple times);
Check if your chosen reference appears multiple times in the file.
To disambiguate a line:
  - Find a unique alternative nearby (preferred).
  - Use a *context-relative line number*
To disambiguate an identifier:
  - Use the *parent chain*: prepend one or more parent names to the identifier name, as in `MyClass.MyOtherClass.my_method`
</li>
<li>Common mistakes:
<context-relative-line-numbers>
Incorrect: Start counting at the function/method's body
Correct: Start counting at the first line where the function/method's signature appears.
</context-relative-line-numbers>
<from-keyword-ordering>
# FROM keyword must directly be followed by keyword `FILE` or `PROJECT`, never by `CLASS`, `FUNCTION` or other keywords.
1) Incorrect: `FROM` followed by `CLASS`, as in `UPDATE FILE "file.py" REPLACE FUNCTION "__init__" FROM CLASS "A"`
   - Correct  : `FROM` keyword followed by `FILE` or `PROJECT`, as in `UPDATE CLASS "A" FROM FILE "file.py" REPLACE FUNCTION "__init__"`
2) Incorrect: `DELETE FUNCTION "something" FROM FILE "my_file.py"`
   - Correct     : `UPDATE FUNCTION "something" FROM FILE "my_file.py" DELETE WHOLE;`
   - Also correct: `UPDATE FILE "my_file.py" DELETE FUNCTION "something";`
   - Also correct: `UPDATE CLASS "MyClass" FROM FILE "my_file.py" DELETE METHOD "something";`
<from-keyword-ordering>
<clause-ordering>
# `FROM` clause *must* come *before* an *action* clause like `DELETE`, `MOVE`, `INSERT`, `REPLACE`.
- Incorrect: UPDATE, REPLACE, FROM, as in `UPDATE FILE "file.py" REPLACE FUNCTION "__init__" FROM CLASS "A"`
- Correct  : UPDATE, FROM, REPLACE, as in `UPDATE CLASS "A" FROM FILE "file.py" REPLACE FUNCTION "__init__"`
</clause-ordering>
<action-clause-without-main-clause>
# Any *action* clause like `DELETE`, `MOVE`, `INSERT` etc *MUST* be preceded by its main clause (`UPDATE`).
- Incorrect: `UPDATE FILE "file.py" DELETE LINE "print(a)"; DELETE LINE "print(b)";`
- Correct: `UPDATE FILE "file.py" DELETE LINE "print(a)"; UPDATE FILE "file.py" DELETE LINE "print(b)";`
</action-clause-without-main-clause>
<triple-backtick>
# When using *triple backticks*, you *MUST* pair *every single backtick* with a preeding backslash (total of 3 pairs of backslash-backtick).
- Incorrect (without a preceding \\ for each backtick): `WITH CONTENT '''Bash: ``` rm *.py ```''';`
- Correct (ever single backtick is preceded by a "\\"): `WITH CONTENT '''Bash: \\`\\`\\` rm *.py \\`\\`\\`''';`
</triple-backtick>
</li>
</ul>

{lazy_prompt}
ONLY EVER RETURN CODE IN *CEDARScript block*!
CEDARScript commands MUST BE *AS CONCISE AS POSSIBLE*!
ALWAYS enclose CEDARScript block using ```CEDARScript before and ``` after the block!
You MUST write <NOCEDARSCRIPT/> as the last line if:
1) You just want *show* some CEDARScript commands to the user instead of executing them;
2) If there are no CEDARScript blocks to execute.
{shell_cmd_reminder}
"""

    example_messages = CEDARScriptPromptsBase.example_messages + [
        dict(
            role="user",
            content="""
'''python
def calculate_sum(a, b):
    return a + b
'''
Add docstring to the function
            """
        ),
        dict(
            role="assistant",
            content="""
{fence[0]}CEDARScript
UPDATE FILE "/dev/stdin"
INSERT INTO FUNCTION "calculate_sum" TOP -- Using `INTO FUNCTION .. TOP` is the *BEST* option to point to add content to the top of the body.
-- The CONTENT below uses the body (the `INTO`) of the function as indent level reference
WITH CONTENT '''
@0:\"\"\"Calculate sum of two numbers.
@0:
@0:Args:
@1:a: First number
@1:b: Second number
@0:
@0:Returns:
@1:Sum of a and b
\"\"\"
''';
{fence[1]}
""",
        ),
        dict(
            role="user",
            content="""
'''python
def something():
    pass


def calculate_sum(a, b):
    return a + b
'''
Add docstring to the function calculate_sum (but don't use `INTO FUNCTION`, as I want to see alternatives)
            """
        ),
        dict(
            role="assistant",
            content="""Alas! That would've been the best command for that, but we do have alternatives. \
Let's use *context-relative line numbers*, which is still an excellent choice.
Note: As the indent level reference is now the function definition instead of its body, we also need to increment by 1 all relative indents.

{fence[0]}CEDARScript
UPDATE FUNCTION "calculate_sum" -- this is the contex for line numbers. Line counting starts 
FROM FILE "/dev/stdin"
INSERT AFTER LINE 1 -- This is the context-relative line number. Line 1 is where the definition for the identifier `calculate_sum` starts 
-- The CONTENT below uses `LINE 1` (*not* the line after it) as indent level reference
WITH CONTENT '''
@1:\"\"\"Calculate sum of two numbers.
@1:
@1:Args:
@2:a: First number
@2:b: Second number
@1:
@1:Returns:
@2:Sum of a and b
\"\"\"
''';
{fence[1]}
""",
        ),
        dict(
            role="user",
            content="""
'''python
def something():
    pass


def calculate_sum(a, b):
    return a + b
'''
Add docstring to the function calculate_sum (but don't use `INTO FUNCTION` nor `LINE 1`, as I want to see alternatives)
            """
        ),
        dict(
            role="assistant",
            content="""We still have many options! The next best one would be to use `BEFORE LINE 2` \
(which points exactly to the same location as `AFTER LINE 1`, albeit with a different relative indent level):

{fence[0]}CEDARScript
UPDATE FUNCTION "calculate_sum" -- this is the contex for line numbering
FROM FILE "/dev/stdin"
INSERT BEFORE LINE 2 -- This is the context-relative line number. Line 2 is where the *body* starts (it's `return a + b`)
-- The CONTENT below uses `LINE 2` (*not* the line before it) as indent level reference
WITH CONTENT '''
@0:\"\"\"Calculate sum of two numbers.
@0:
@0:Args:
@1:a: First number
@1:b: Second number
@0:
@0:Returns:
@1:Sum of a and b
\"\"\"
''';
{fence[1]}
""",
        ),
        dict(
            role="user",
            content="""
'''python
def a():
    def calculate_sum(a, b):
        return a + b
def b():
    def calculate_sum(a, b):
        return a + b
'''
Add docstring to the function calculate_sum nested inside b. \
Briefly explain your selection of reference points for code locations.
            """
        ),
        dict(
            role="assistant",
            content="""We cannot simply use `FUNCTION "calculate_sum"`, as its name appears multiple times in the provided script. \
Let's use the `parent chain` to easily disambiguate it:

{fence[0]}CEDARScript
UPDATE FILE "/dev/stdin"
INSERT INTO FUNCTION "b.calculate_sum" TOP -- the function to be modified has `b` as its direct parent
WITH CONTENT '''
@0:\"\"\"Calculate sum of two numbers.
@0:
@0:Args:
@1:a: First number
@1:b: Second number
@0:
@0:Returns:
@1:Sum of a and b
\"\"\"
''';
{fence[1]}
""",
        ),
        dict(
            role="user",
            content="""
'''python
class A:
    def calculate_sum(self, a, b):
        return a + b
class B:
    def calculate_sum(self, a, b):
        return a + b
'''
Add docstring to the method in class B. Don't use `parent chain`, as I want to see alternatives.
            """
        ),
        dict(
            role="assistant",
            content="""We can also use `UPDATE CLASS "B"` as a way to disambiguate the method: it will match any \
level of nesting for the method, but since the method is unique inside class `B`, we can still use it.
The parent chain "B.calculate_sum" is more precise (matches the method having class `B` as its direct parent),
but in this particular case we don't require it.
{fence[0]}CEDARScript
UPDATE CLASS "B"
FROM FILE "/dev/stdin"
INSERT INTO METHOD "calculate_sum" TOP -- matches the method at any level of nesting inside class `B`
WITH CONTENT '''
@0:\"\"\"Calculate sum of two numbers.
@0:
@0:Args:
@1:a: First number
@1:b: Second number
@0:
@0:Returns:
@1:Sum of a and b
\"\"\"
''';
{fence[1]}
""",
        ),
        dict(
            role="user",
            content="""
'''python
def something():
    pass

class A:
    def a(self, a1):
        c, d = self.b(a1x)
        if a1 > 0:
            c = "x" + a1
        return 1,2
    def b(self, a1):
        c, d = self.b(a1x)
        if a1 > 0:
            c = "x" + a1
        return 1,2
'''
a1x is a mistake. It should be a1
            """
        ),
        dict(
            role="assistant",
            content="""{fence[0]}CEDARScript
UPDATE METHOD "a" -- this is the contex for line numbering
FROM FILE "/dev/stdin"
REPLACE LINE 2 -- Line counting starts at `def a(self, a1):`, so line 2 is where the *body* starts (it's `c, d = self.b(a1x)`)
-- The CONTENT below uses `LINE 2` as indent level reference
WITH CONTENT '''
@0:c, d = self.b(a1)
''';
UPDATE METHOD "b" -- this is the contex for line numbering
FROM FILE "/dev/stdin"
REPLACE LINE 2 -- Line counting starts at `def a(self, a1):`, so line 2 is where the *body* starts (it's `c, d = self.b(a1x)`)
-- The CONTENT below uses `LINE 2` as indent level reference
WITH CONTENT '''
@0:c, d = self.b(a1)
''';
{fence[1]}
""",
        ),
        dict(
            role="user",
            content="""
'''python
class MyClass(NamedTuple):
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
        b = checkVal(45, "strict", self.myFirstFunction(name, age), 8, "tops")
        bb = checkVal(7, "lax", self.myFirstFunction(name, age), 2, "bottom")
        c = "x" + '"' + "'" + "z"
        print("calc d...")
        d = checkVal(45, "strict", self.myFirstFunction(name, age), 8, "tops")
        print("calc dd...")
        print("takes longer...")
        dd = checkVal(4455, "aasdf", '33se"asd',
          "strict", 8, 
          "tops", "xx",
          '9"f', "as'df", self.myFirstFunction(name, age))
        return b * 3
'''
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
-- 1. Move the `myFirstFunction()` method from the `MyClass` class, placing it at the top level, just before the line where its class starts.
UPDATE FILE "/dev/stdin"
MOVE FUNCTION "myFirstFunction"
INSERT BEFORE CLASS "MyClass"
  RELATIVE INDENTATION 0; -- the function being moved will start at the same indentation as the class `MyClass`

-- 2. Update the copied function to remove references to `self`, now declaring `instance_var_1` as parameter
UPDATE FUNCTION "myFirstFunction"
  FROM FILE "/dev/stdin"
REPLACE LINE 2
WITH CONTENT '''
@0:instance_var_1: str, name: str,
''';
UPDATE FUNCTION "middle" -- We're only using it as a unique reference point to reach `myFirstFunction`
FROM FILE "/dev/stdin"
REPLACE LINE 0 -- the line BEFORE function `middle`, that is, the last line of `myFirstFunction`
-- `@0:` is used because LINE 0 is the return statement of `myFirstFunction`
WITH CONTENT '''
@0:return a + 5 + len(instance_var_1) * 7
''';

-- 3. Update ALL call sites of the method `myFirstFunction` to call the new top-level function with the same name, passing `instance_var_1` as argument
UPDATE FUNCTION "anotherFunction"
FROM FILE "/dev/stdin"
REPLACE SEGMENT
  STARTING AT LINE 2 -- "b = checkVal" ...
  ENDING AT LINE 3 -- "bb = checkVal" ...
WITH CONTENT '''
@1:b = checkVal(45, "strict", myFirstFunction(instance_var_1, name, age), 8, "tops")
@1:bb = checkVal(7, "lax", myFirstFunction(instance_var_1, name, age), 2, "bottom")
''';
UPDATE FUNCTION "anotherFunction"
FROM FILE "/dev/stdin"
REPLACE LINE 6 -- "d = checkVal" ...
WITH CONTENT '''
@0:d = checkVal(45, "strict", myFirstFunction(instance_var_1, name, age), 8, "tops")
''';
UPDATE FUNCTION "anotherFunction"
FROM FILE "/dev/stdin"
REPLACE LINE 12
WITH CONTENT '''
@0:'9"f', "as'df", myFirstFunction(instance_var_1, name, age))
''';
{fence[1]}

Notes:
1. As the code to be changed was provided in your message, we're using file name "/dev/stdin".
""",
        ),
        dict(
            role="user",
            content="""
'''python
class MyClass(NamedTuple):
    instance_var_1: str = '4r3'
    def myFirstFunction(self, name: str, age: int):
        \"\"\"Lorem ipsum dolor sit amet
        Args:
            name: name
            age: age
        \"\"\"
        if age > 70
          a = doSomething(name, age)
          return a + 5 + len(self.instance_var_1) * 7
      def middle(self):
          pass
      def anotherFunction(self, name: str, age: int):
          # Check and store in 'b' and 'bb'
          b = checkVal(45, "strict", self.myFirstFunction(name, age), 8, "tops")
          bb = checkVal(7, "lax", self.myFirstFunction(name, age), 2, "bottom")
          return b + bb
  '''
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
UPDATE FILE "/dev/stdin"
MOVE FUNCTION "myFirstFunction"
INSERT BEFORE CLASS "MyClass"
  RELATIVE INDENTATION 0; -- the block of code being moved wil start at the same indentation as the 'reference mark'

-- 2. Update the copied function to remove references to `self`, now declaring `instance_var_1` as parameter
UPDATE FUNCTION "myFirstFunction"
  FROM FILE "/dev/stdin"
REPLACE LINE 1
WITH CONTENT '''
@0:def myFirstFunction(instance_var_1: str, name: str, age: int):
''';
UPDATE FUNCTION "middle" -- We're only using it as a unique reference point to reach `myFirstFunction`
  FROM FILE "/dev/stdin"
REPLACE LINE 0 -- the line BEFORE function `middle`, that is, the last line of `myFirstFunction`
-- `@0:` is used because LINE 0 is the return statement of `myFirstFunction`
WITH CONTENT '''
@0:return a + 5 + len(instance_var_1) * 7
''';

-- 3. Update ALL call sites of the method `myFirstFunction` to call the new top-level function with the same name, passing `instance_var_1` as argument
UPDATE FUNCTION "anotherFunction"
FROM FILE "/dev/stdin"
REPLACE SEGMENT
  STARTING AT LINE 3 -- "b = checkVal" ...
  ENDING AT LINE 4 -- "bb = checkVal" ...
WITH CONTENT '''
@0:b = checkVal(45, "strict", myFirstFunction(instance_var_1, name, age), 8, "tops")
@0:bb = checkVal(7, "lax", myFirstFunction(instance_var_1, name, age), 2, "bottom")
''';
{fence[1]}

Notes:
1. As the code to be changed was provided in your message, we're using file name "/dev/stdin".
""",
        ),
        dict(
            role="user",
            content="""
'''python
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
'''

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
UPDATE CLASS "Greeter" -- As method `__init__` exists in more than 1 class, we specify which one we want to reference
  FROM FILE "/dev/stdin"
REPLACE METHOD "__init__" -- Replace the entire method, as there's nothing to keep
WITH CONTENT '''
@0:def __init__(self):
@1:self.greeting_count: int = 0
''';

-- 2. Implement the `print_with_prefix()` method to print parameter `name` prefixed with the `prefix` parameter;
UPDATE CLASS "Greeter" -- As method `print_with_prefix` exists in more than 1 class, we specify which one we want to reference
  FROM FILE "/dev/stdin"
REPLACE METHOD "print_with_prefix" -- no need to preserve it, so we replace it
WITH CONTENT '''
@0:def print_with_prefix(self, prefix: str, name: str):
@1:print(f"{{prefix}}{{name}}")
''';

-- 3. Insert a call to the `print_with_prefix()` method at the top of the last method (`greet`);
UPDATE CLASS "Greeter" -- As method `greet` exists in more than 1 class, we specify which one we want to reference
  FROM FILE "/dev/stdin"
INSERT INTO METHOD "greet" TOP -- at the TOP of the function body
-- The function body is the reference indent level; `@0:` means to use that same level 
WITH CONTENT '''
@0:print_with_prefix('Hi, ', name)
''';

-- 4. Insert code at the bottom of the `greet()` method to increment the greeting count and print it.
UPDATE CLASS "Greeter" -- As method `greet` exists in more than 1 class, we specify which one we want to reference
  FROM FILE "/dev/stdin"
INSERT INTO METHOD "greet" BOTTOM -- at the BOTTOM of the function body
-- The function body is the reference indent level; `@0:` means to use that same level 
WITH CONTENT '''
@0:self.greeting_count += 1
@0:print(f'There have been {{self.greeting_count}} greetings so far.')
''';
{fence[1]}

Notes to self:
1. As the code to be changed was provided in the message, we're using file name "/dev/stdin".
2. When using `INTO`, the body of the function or class is implicit, so we can NEVER write `BODY` after `INTO`.
""",
        ),
        dict(
            role="user",
            content="""'''python
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
'''
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
UPDATE CLASS "A" -- As method `calc1` exists in more than 1 class, we specify which one we want to reference
  FROM FILE "/dev/stdin"
MOVE METHOD "calc1"
INSERT BEFORE CLASS "A"
  RELATIVE INDENTATION 0;

-- 2. Update the copied function to remove references to `self`, now declaring `instance_var` as parameter
UPDATE FUNCTION "calc1" OFFSET 1 -- Now, `calc1` exists as a top-level function before class `A` (we just moved it), but there's also a method with the same name inside class `A0`, so we use `OFFSET 1` to skip the first match (the one from `A0`)
  FROM FILE "/dev/stdin"
REPLACE LINE '''def calc1(self, a):'''
WITH CONTENT '''
@0:def calc1(instance_var: int, a):
''';
UPDATE FUNCTION "calc1" OFFSET 1 -- to skip 1 match (the one from `A0`)
  FROM FILE "/dev/stdin"
REPLACE LINE \"\"\"after 'self') by a value stored in 'self.instance_var'.\"\"\"
WITH CONTENT '''
@0:after 'instance_var') by a value stored in 'instance_var'.
''';
UPDATE FUNCTION "calc1" OFFSET 1 -- to skip 1 match (the one from `A0`)
  FROM FILE "/dev/stdin"
REPLACE LINE '''return a * self.instance_var'''
WITH CONTENT '''
@0:return a * instance_var
''';

-- 3. Update ALL call sites of the method `calc1` to call the new top-level function with the same name, passing `instance_var` as argument
UPDATE FUNCTION "calc2" OFFSET 1 -- There are 2 `calc2` methods. We skip 1, meaning we target the second one (which is the one in the `A` class)
  FROM FILE "/dev/stdin"
REPLACE LINE 'c = self.calc1(' -- There's only 1 call site, so it's more concise to just replace a line instead of the whole `calc2` contents
WITH CONTENT '''
@0:c = calc1(self.instance_var,
''';
{fence[1]}""",
        ),
    dict(
            role="user",
            content="""'''python
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
        print(a)
        # Call calc1...
        c = ["x", str(self.calc1(
            5), "xx"]
        c = ["x", str(self.calc1(
            6), "xx"]
        # Done...
        return c
'''
Refactor the `calc1` method in the `A` class to be a stand alone, top level function. Also, there's a line that clearly needs to be removed.
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
UPDATE CLASS "A" -- As method `calc1` exists in more than 1 class, we specify which one we want to reference
  FROM FILE "/dev/stdin"
MOVE METHOD "calc1"
INSERT BEFORE CLASS "A"
  RELATIVE INDENTATION 0;

-- 2. Replace the whole copied function to remove references to `self` and declare `instance_var` as parameter
UPDATE FUNCTION "calc1" OFFSET 1 -- Now, `calc1` exists as a top-level function before class `A` (we just moved it), but there's also a method with the same name inside class `A0`, so we use `OFFSET 1` to skip the first match (the one from `A0`)
  FROM FILE "/dev/stdin"
REPLACE WHOLE -- It's better to replace the whole function because the function is small
WITH CONTENT '''
@0:def calc1(instance_var: int, a):
@1:return a * instance_var
''';

-- 3. Update ALL call sites of the method `calc1` to call the new top-level function with the same name, passing `instance_var` as argument
UPDATE FUNCTION "A.calc2"
  FROM FILE "/dev/stdin"
REPLACE LINE 5
WITH CONTENT '''
@0:c = ["x", str(calc1(self.instance_var,
''';
UPDATE FUNCTION "calc2" OFFSET 1
  FROM FILE "/dev/stdin"
REPLACE LINE 7
WITH CONTENT '''
@01:c = ["x", str(calc1(self.instance_var,
''';
-- Note to self: A line marker referencing 'c = ["x", str(self.calc1(' would be ambiguous, since there are 2 or more \
matches for it. Thus, it's important to use context-relative line numbers.

-- 4. Delete the bad line
UPDATE FILE "/dev/stdin"
DELETE LINE "# I'm a bad line, get rid of me!";
{fence[1]}""",
        ),
    dict(
            role="user",
            content="""'''python
def calc1(a):
    return a * 7.0
def calc2(a):
    c = ["x", str(calc1(
        5), "xx"]
    c = ["x", str(calc1(
        6), "xx"]
    # Done...
    return c
'''
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
  FROM FILE "/dev/stdin"
REPLACE WHOLE
WITH CONTENT'''
@0:def calc1(tax: float, a):
@1:return a * tax
''';

-- 2. Update the function signature of `calc2()` to add parameter `base_tax: float = 1.3` as the last one
UPDATE FUNCTION "calc2"
  FROM FILE "/dev/stdin"
REPLACE LINE 1
WITH CONTENT'''
@0:def calc2(a, base_tax: float = 1.3):
''';

-- 3. Update ALL call sites of `calc1()` to pass `base_tax` as the first argument
UPDATE FILE "/dev/stdin"
REPLACE LINE 2
WITH CONTENT '''
@0:c = ["x", str(calc1(base_tax,
''';
UPDATE FUNCTION "calc2"
  FROM FILE "/dev/stdin"
REPLACE LINE 4
WITH CONTENT '''
@0:c = ["x", str(calc1(base_tax,
''';
-- Note to self: A line marker referencing 'c = ["x", str(calc1(' would be ambiguous, since there are 2 or more \
matches for it. Thus, it's important to use context-relative line numbers.
{fence[1]}""",
        ),
    dict(
            role="user",
            content="""'''python
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
                    self._candidate(
                        a, "string 1", 4
                    )
                    for index, item in enumerate(a.the_elements)
                )
            )

    def _candidate(self, a, b, c):
        return a
'''
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
UPDATE FILE "/dev/stdin"
MOVE METHOD "_candidate" -- As method `_candidate` only exists in one place, it's unambiguous, so we ought to directly reference it
INSERT BEFORE CLASS "A"
  RELATIVE INDENTATION 0;

-- 2. Update the copied function to remove references to `self`
UPDATE FUNCTION "_candidate"
  FROM FILE "/dev/stdin"
REPLACE LINE 1
WITH CONTENT '''
@0:def _candidate(a, b, c):
''';

-- 3. Update ALL call sites of the method `_candidate()` to call the new top-level function with the same name
UPDATE METHOD "_check"
  FROM FILE "/dev/stdin"
REPLACE LINE '''self._candidate(''' -- There's only 1 call site and this line marker is unambiguous
WITH CONTENT '''
@0:_candidate(
''';
{fence[1]}""",
        ),
    dict(
            role="user",
            content="""'''python
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
                    self._candidate(
                        a, "string 1", 4
                    )
                    for index, item in enumerate(a.the_elements)
                )
            )

    def _candidate(self, a, b, c):
        return a
'''
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
UPDATE CLASS "A" -- As method `_candidate` only exists in one place, it's unambiguous, but this time we wmust try the alternative form `UPDATE CLASS..MOVE FUNCTION` (instead of `UPDATE FUNCTION..MOVE WHOLE`) because the latter failed last time we tried.
  FROM FILE "/dev/stdin"
MOVE METHOD "_candidate"
INSERT BEFORE CLASS "A"
  RELATIVE INDENTATION 0;

-- 2. Update the copied function to remove references to `self`
UPDATE FUNCTION "_candidate"
  FROM FILE "/dev/stdin"
REPLACE LINE 1
WITH CONTENT '''
@0:def _candidate(a, b, c):
''';

-- 3. Update ALL call sites of the method `_candidate()` to call the new top-level function with the same name
UPDATE METHOD "_check"
  FROM FILE "/dev/stdin"
REPLACE LINE '''self._candidate(''' -- There's only 1 call site and this line marker is unambiguous
WITH CONTENT '''
@0:_candidate(
''';
{fence[1]}""",
        ),
    ]
