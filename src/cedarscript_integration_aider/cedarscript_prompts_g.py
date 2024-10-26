# flake8: noqa: E501

from .cedarscript_prompts_base import CEDARScriptPromptsBase


class CEDARScriptPromptsGrammar(CEDARScriptPromptsBase):

    def edit_format_name(self):
        return f"{super().edit_format_name()}-g"

    final_remarks = CEDARScriptPromptsBase.final_remarks_brain

    edit_format_training = """<training><p>Learning CEDARScript</p>
Please read the tree-sitter grammar rules (enclosed by <grammar.js> tags) to learn the syntax and how to use CEDARScript:
<grammar.js>
const SELECT_FILENAMESPATHS_TARGET = seq('FILE', choice('NAMES', 'PATHS'))
const SELECT_OTHER_TARGETS = choice(
  seq('FILE', 'CONTENTS'),
  seq('CLASS', choice('NAMES', 'CONTENTS')),
  seq('FUNCTION', choice('NAMES', 'SIGNATURES', 'CONTENTS')),
  seq('VARIABLE', choice('NAMES', 'CONTENTS')),
  'IDENTIFIERS'
);
/**
- WHOLE: the whole chosen item;
- BODY: Only the function body (its *signature* is *NOT* considered);
*/
const BODY_OR_WHOLE = field('bow', choice('BODY', 'WHOLE'))

/**
<about>CEDARScript, SQL-like language used to express code manipulations (via DDL and DML Write commands) and to help an LLM examine and understand the codebase (via DML Read-Only command)</about>
*/
module.exports = grammar({
  name: 'CEDARScript',

  extras: $ => [
    /\\s|\\r?\\n/,
    $.comment
  ],

  rules: {
    source_file: $ => repeat(seq(
      $._command,
      optional($.command_separator)
    )),

    _command: $ => choice(
      // DDL
      $.create_command,
      $.rm_file_command,
      $.mv_file_command,
      // DML (write)
      $.update_command,
      // DML (Read-Only)
      $.select_command,
      prec(-1, alias($.invalid_move_command, $.error))
    ),
    invalid_move_command: $ => seq(
      'MOVE',
      choice('FILE', 'FUNCTION', 'CLASS', 'VARIABLE'),
    ),
    /**
    Syntax: CREATE FILE "<path/to/new-file>" WITH CONTENT '''<content>''';
    Only for new files. Fails if file already exists.
    */
    create_command: $ => seq(
      'CREATE', $.singlefile_clause,
      'WITH', $.content_clause
    ),

    /**
    Syntax: RM FILE "<path/to/file>";
    Use cases: Delete file from the codebase
    */
    rm_file_command: $ => seq(
      'RM', $.singlefile_clause
    ),

    /**
    Syntax: MV FILE "<source-file>" TO "<target-file>";
    Use cases: Renaming a file, moving a file to another path (target file is overwritten if existing).
    <example><goal>Rename "old.js", then move "config.json" to "production" folder</goal>
    ```CEDARScript
    -- Rename "old.js"
    MV FILE "src/old.js" TO "src/new.js";
    -- Overwrite development config with production config
    MV FILE "production/config.ini" TO "development/config.ini";
    ```
    </example>
    */
    mv_file_command: $ => seq(
      'MV', $.singlefile_clause, $.to_value_clause
    ),

    /**
    Syntax (simplified): UPDATE <singlefile or identifier_from_file> <update type>;
    <use-cases>
    - Creating or replacing classes, functions or other code in existing files/classes/functions
    - Replacing specific lines of existing code
    - Performing complex code transformations using refactoring patterns
    - etc...
    </use-cases>
    */
    update_command: $ => seq(
      'UPDATE',
      choice(
        field('singleFile_clause',
          seq(
            $.singlefile_clause,
            choice(
              $.update_delete_region_clause,
              $.update_move_mos_clause,
              seq(
                choice(
                  $.insert_clause,
                  $.replace_region_clause
                ),
                seq('WITH', choice($.content_clause, $.content_from_segment))
              )
            )
          )
        ),
        field('identifierInFile_clause',
          seq(
            $.identifier_from_file,
            choice(
              $.update_delete_region_clause,
              $.update_move_region_clause,
              seq(
                choice(
                  $.insert_clause,
                  $.replace_region_clause
                ),
                seq('WITH', choice($.content_clause, $.content_from_segment))
              )
            )
          )
        ),
        $.update_project_clause
      )
    ),

    insert_clause: $ => seq('INSERT', $.relpos_bai),

    /**
    Define what to be replaced in the chosen function, class or file.
    */
    replace_region_clause: $ => seq('REPLACE', $.region_field),
    // ---

    /**
    refactor_language_field: Only language 'rope' is supported. Works only with Python codebases.
    */
    refactor_language_field: $ => seq('REFACTOR LANGUAGE', field('refactor_language', $.string)),
    pattern_field: $ => seq('PATTERN', field('pattern', $.string)),
    goal_field: $ => seq('GOAL', field('goal', $.string)),

    /**
    update_delete_region_clause: *NOT* top-level command. Used inside the `UPDATE` command to specify deletion of code parts.
    */
    update_delete_region_clause: $ => seq('DELETE', $.region_field),
    // ---

    /**
    update_project_clause: Advanced pattern-based refactorings.
    Indirectly use the `Restructure` class in the 'Rope' refactoring library to perform complex code transformations using patterns.
    These patterns can match and replace code structures in your project.
    */
    update_project_clause: $ => seq('PROJECT', $.refactor_language_field,
      'WITH', $.pattern_field,
      'WITH', $.goal_field,
    ),
    update_move_clause_destination: $ => field('move_destination', seq(
      optional(seq('TO', $.singlefile_clause)), // `TO` can ONLY be used if it points to a different file
      $.insert_clause,
      optional($.relative_indentation)
    )),

    // update_move_mos_clause, update_move_region_clause
    /**
    `MOVE` is only used as part of the UPDATE command for moving code within a file.
    Unlike CREATE, RM, or UPDATE, it is *NOT* a top-level command.
    */
    update_move_mos_clause: $ => seq('MOVE', field('move_mos_source', $.marker_or_segment), $.update_move_clause_destination),
    update_move_region_clause: $ => seq('MOVE', field('move_region_source', $.region_field), $.update_move_clause_destination),
    // ---

    /**
    Syntax: (VARIABLE|FUNCTION|CLASS) "<name>" [OFFSET <offset>] FROM FILE "<path/to/file>"
    Use cases: Specify an identifier in a given file.
    <params>
    - `<name>`: Identifies the name of a variable, function or class as the item of interest in the file.
    - `<offset>`: Specifies how many items to skip. Mandatory when there are 2 or more matching elements. See details in `offset_clause`.
    </params>
    */
    identifier_from_file: $ => seq(
      $.identifierMarker, 'FROM', $.singlefile_clause,
      optional($.where_clause)
    ),

    /**
    Read-only command. Used to glean information about the code base being examined.
    <use-cases>
    - Understanding code structure;
    - Finding relevant files/classes/functions/variables that may deal with a certain topic
       -- (ex.: if a user may want to find all places that deal with payments, search for 'payment')
    - Displaying code elements to user
    - Generating documentation;
    - Automating code navigation.
    </use-cases>
    */
    select_command: $ => seq(
      'SELECT',
      choice(
        seq(field('file_names_paths_target', $.select_filenamespaths_target), 'FROM', $.multifile_clause),
        seq(field('single_or_multifile_target', $.select_other_target), 'FROM', choice($.singlefile_clause, $.multifile_clause))
      ),
      optional($.where_clause),
      optional($.limit_clause)
    ),

    select_filenamespaths_target: $ => SELECT_FILENAMESPATHS_TARGET,
    select_other_target: $ => SELECT_OTHER_TARGETS,

    where_clause: $ => seq(
      'WHERE',
      field('condition', $.condition)
    ),

    conditions_left: $ => choice(
      'NAME',
      'PATH'
    ),
    operator: $ => choice('=', 'LIKE'),
    condition: $ => seq($.conditions_left, $.operator, field('value_or_pattern', $.string)),

    to_value_clause: $ => seq('TO', field('value', $.single_quoted_string)),
    /**
    Syntax: FILE "<path/to/file>"
    Use cases: Specify a file
    */
    singlefile_clause: $ => seq('FILE', field('path', $.string)),
    multifile_clause: $ => seq(
      choice('PROJECT', seq('DIRECTORY', field('directory', $.single_quoted_string))),
      optional($.maxdepth_clause)
    ),

    maxdepth_clause: $ => seq('MAX DEPTH', field('depth', $.number)),

    // <specifying-locations-in-code>
    /**
    lineMarker: Points to specific line via its trimmed contents. You *MUST* strip whitespace from left and right of the value!
    *NEVER* use an ambiguous line (one that appears 2 or more times) as reference. Instead, prefer a different, nearby line.
    */
    lineMarker: $ => seq('LINE', field('lineMarker', $.string), optional($.offset_clause)),
    /**
    identifierMarker: Points to an identifier (variable, function or class).
    Use `OFFSET <n>` to pinpoint which (if there are 2 or more with same name)
    */
    identifierMarker: $ => seq(field('identifier', choice('VARIABLE', 'FUNCTION', 'CLASS')), field('identifierMarker', $.string), optional($.offset_clause)),
    marker: $ => choice($.lineMarker, $.identifierMarker),
    /**
    relpos_beforeafter: Points to region immediately before or after a `marker`
    */
    relpos_beforeafter: $ => field('relpos_beforeafter', seq(choice('BEFORE', 'AFTER'), $.marker)),
    /**
    relpos_inside: Points to inside `identifierMarker` (either the body's TOP or BOTTOM region). The reference indentation level is the body's.
    Syntax: INSIDE (FUNCTION|CLASS) "<name>" [OFFSET <offset>] (TOP|BOTTOM)
    Use cases: When inserting content either at the TOP or BOTTOM of a function or class body.
    Examples: <ul>
    <li>INSIDE FUNCTION my_function OFFSET 1 BOTTOM -- at the BOTTOM of the function body</li>
    <li>INSIDE FUNCTION my_function TOP -- at the TOP of the function body</li>
    </ul>
    */
    relpos_inside: $ => seq('INSIDE', field('inside', $.identifierMarker), field('topOrBottom', choice('TOP', 'BOTTOM'))),
    relpos_bai: $ => field('relpos_bai', choice($.relpos_beforeafter, $.relpos_inside)),
    /**
    relpos_at: points to a specific `lineMarker`
    */
    relpos_at: $ => seq('AT', field('at', $.lineMarker)),
    /**
    relpos_segment_start: Points to start of segment
    */
    relpos_segment_start: $ => seq('STARTING', field('starting', choice($.relpos_at, $.relpos_beforeafter))),
    /**
    relpos_segment_end: Points to end of segment
    */
    relpos_segment_end: $ => seq('ENDING', field('ending', choice($.relpos_at, $.relpos_beforeafter))),
    /**
    segment: Points to segment identified by a start and an end pointer
    */
    segment: $ => field('segment', seq('SEGMENT', $.relpos_segment_start, $.relpos_segment_end)),
    marker_or_segment: $ => field('mos', choice($.marker, $.segment)),
    /** region_field:
    - BODY_OR_WHOLE: pre-defined regions
    - marker_or_segment: more flexible region selection
    */
    region_field: $ => field('region', choice(BODY_OR_WHOLE, $.marker_or_segment)),

    /**
    Field `offset`: Integer to identify how many matches to skip. *MANDATORY* iff there are 2 or more matching elements.
    <examples>
    <li>`OFFSET 0` is the default when there's only one matching element. It means to skip 0 items (so, points to the *1st* match).</li>
    <li>`OFFSET 1` skips 1 matches, so points to the *2nd* matches</li>
    <li>`OFFSET 2` skips 2 matches, so points to the *3rd* matches</li>
    <li>`OFFSET n` skips n matches, thus specifies the (n+1)-th matches</li>
    </examples>
    */
    offset_clause: $ => seq('OFFSET', field('offset', $.number)),

    // </specifying-locations-in-code>

    limit_clause: $ => seq('LIMIT', field('count', $.number)),

    /**
    relative_indentation: Helps maintain proper code structure when inserting or replacing code.
    Sets the indentation level relative to the context specified in the command:
    <li>`INSIDE (FUNCTION|CLASS)`: Reference is the body of the function or class</li>
    <li>`(BEFORE|AFTER) (LINE|FUNCTION|CLASS)`: Reference is line, function, or class, regardless of whether BEFORE or AFTER is used</li>
    When `rel_indent` is 0, code is put at the same level as the reference.
    */
    relative_indentation: $ => seq('RELATIVE INDENTATION', field('rel_indent', $.number)),

    content_from_segment: $ => seq(
      optional($.singlefile_clause),
      $.marker_or_segment,
      optional($.relative_indentation)
    ),

    /**
<details topic="Relative Indent Strings">
<summary>A relative indent prefix is used within strings in CONTENT blocks to simplify matching indentation with the existing code being changed</summary>
<p>Syntax:</p>
<ol>
<li>`@N:` is the relative indent prefix</li>
<li>`N` is an integer representing the relative indent *level* (can be negative)</li>
<li>`content` is the actual code or text for that line</li>
</ol>
<examples>
<li>'@7:single-quote-string'</li>
<li>"@-3:double-quote-string"</li>
<li>r"@0:raw-string"</li>
<li>'''
@0:multi
@-1:line
'''</li>
<li>\"\"\"
@0:multi
@-1:line
\"\"\"</li>
</examples>

<p>Key points:</p>
<ol>
<li>Each line must start with `@N:` where `N` represents the indentation level</li>
<li>Indentation level *MUST* change logically with code structure:
   - *MUST* increment N when entering a new block (class body, function body, if statement, loop, etc.)
   - *MUST* Decrement N when exiting a block
 </li>
<li>The actual content follows immediately after the prefix (@N:)</li>
</ol>

<example>
[...] WITH CONTENT '''
@0:class myClass:
@1:def myFunction(param):
@2:if param > 0:
@3:print("Positive")
@2:else:
@3:print("Non-positive")
@2:return param * 2
@0:class nextClass:
'''
</example>

Remember: The relative indentation prefix (@N:) is used to indicate the logical structure
of the code. The CEDARScript interpreter will handle the actual formatting and indentation
in the target code file.
    */
    content_clause: $ => seq('CONTENT', field('content', $.string)),

    escape_sequence: $ => token(seq(
      '\\\\',
      choice(
        /[abfnrtv\\\\"']/,
        /\\d{1,3}/,
        /x[0-9a-fA-F]{2}/,
        /u[0-9a-fA-F]{4}/,
        /U[0-9a-fA-F]{8}/,
        /N\\{[^}]+\\}/
      )
    )),

    string: $ => choice(
      $.raw_string,
      $.single_quoted_string,
      $.multi_line_string
    ),
    raw_string: $ => choice(
      seq(
        'r"',
        repeat(/./),
        '"'
      ),
      seq(
        "r'",
        repeat(/./),
        "'"
      ),
      seq(
        'r\"\"\"',
        repeat(/./),
        '\"\"\"'
      ),
      seq(
        "r'''",
        repeat(/./),
        "'''"
      )
    ),
    single_quoted_string: $ => choice(
      seq(
        "'",
        repeat(choice(
          /[^'\\\\\\n]/,
          $.escape_sequence
        )),
        "'"
      ),
      seq(
        '"',
        repeat(choice(
          /[^"\\\\\\n]/,
          $.escape_sequence
        )),
        '"'
      )
    ),
    /**
    multi_line_string: Also useful to avoid escaping quotes
    */
    multi_line_string: $ => choice(
      seq(
        '\"\"\"',
        repeat(choice(
          /[^"\\\\]/,
          '"',
          '""',
          $.escape_sequence
        )),
        '\"\"\"'
      ),
      seq(
        "'''",
        repeat(choice(
          /[^'\\\\]/,
          "'",
          "''",
          $.escape_sequence
        )),
        "'''"
      )
    ),

    number: $ => /\\d+/,

    comment: $ => token(seq('--', /.*/)),

    command_separator: $ => ';'

  }
});
</grammar.js>
"""

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
<li>Each CEDARScript command is applied in the same order as they appear. If a command fails to be applied, all commands before it were correctly applied (don't retry those!). Once a command is applied on a file, the next command will see the update version of that file, with all changes that were applied by earlier commands.</li>
<li>It's crucial to strive to provide *as concise and small as possible*, targeted CEDARScript commands that each change a given aspect of the program, so that humans can easily understand what's changing</li>
<li>Try *HARD* to minimize the number of unchanged lines in a CEDARScript command and to have a very *concise* script</li>
<li>To move code within a file or identifier (class, method or function), you *MUST* use the `UPDATE ... MOVE ...` construct to minimize script size (DON'T use `WITH CONTENT`)
<IMPORTANT>
1. You wmust try the alternative form `UPDATE CLASS..MOVE FUNCTION` (instead of `UPDATE FUNCTION..MOVE WHOLE`) if the latter fails
2. If there are MULTIPLE identifiers with the same name, you *MUST* choose an appropriate reference that is unambiguous! 
</IMPORTANT>
</li>
<li>Prefer using multiline_string (enclosed in ''') even for single line content (provides better indentation)</li>
<li>For `CONTENT` blocks, ALWAYS use `relative indent prefix` (which is the @N: part) for each line. Understand that the actual indentation characters (spaces or tabs) will be applied by the CEDARScript engine,
adjusting your relative indentation to match the target code's style and position.
<CRUCIAL>
Each line must start with `@N:` where `N` represents the indentation level.
Indentation level *MUST* change logically with code structure:
   - *MUST* increment N when entering a new block (class body, function body, if statement, loop, etc.)
   - *MUST* Decrement N when exiting a block
If you get `E999 IndentationError` message or any other indentation error, it means you forgot these rules.
Examples of correctd usage of `@N:` below:
<example>
<raw>
class A:
    def m1(self):
        pass
    def m2(self):
        if 1 > 1:
            pass
        pass
class B
</raw>
<relative-indent-block>'''
@0:class A:
@1:def m1(self):
@2:pass
@1:def m2(self):
@2:if 1 > 1:
@3:pass
@2:pass
@0:class B
'''</relative-indent-block>
</example>
 </CRUCIAL>
</li>
<li>*NEVER* use an ambiguous line (one that appears 2 or more times) as reference. Instead, prefer a different, nearby line.</li>
<li>Common mistakes:
<from-keyword-misuse>
# FROM keyword must directly be followed by keyword `FILE` or `PROJECT`, never by `CLASS`, `FUNCTION` or other keywords.
1) Incorrect: `FROM` followed by `CLASS`, as in `UPDATE FILE "file.py" REPLACE FUNCTION "__init__" FROM CLASS "A"`
   - Correct  : `FROM` keyword followed by `FILE` or `PROJECT`, as in `UPDATE CLASS "A" FROM FILE "file.py" REPLACE FUNCTION "__init__"`
2) Incorrect: `DELETE FUNCTION "something" FROM FILE "my_file.py"`
   - Correct     : `UPDATE FUNCTION "something" FROM FILE "my_file.py" DELETE WHOLE;`
   - Also correct: `UPDATE FILE "my_file.py" DELETE FUNCTION "something";`
   - Also correct: `UPDATE CLASS "MyClass" FROM FILE "my_file.py" DELETE METHOD "something";`
<from-keyword-misuse>
<clause-ordering>
# `FROM` clause *must* come *before* an *action* clause like `DELETE`, `MOVE`, `INSERT`, `REPLACE`.
- Incorrect: UPDATE, REPLACE, FROM, as in `UPDATE FILE "file.py" REPLACE FUNCTION "__init__" FROM CLASS "A"`
- Correct  : UPDATE, FROM, REPLACE, as in `UPDATE CLASS "A" FROM FILE "file.py" REPLACE FUNCTION "__init__"`
</clause-ordering>
</li>
</ul>

{lazy_prompt}
ONLY EVER RETURN CODE IN *CEDARScript block*!
CEDARScript commands MUST BE *AS CONCISE AS POSSIBLE*!
ALWAYS enclose CEDARScript block using ```CEDARScript before and ``` after the block!
If you want to just *show* some CEDARScript commands to the user instead of executing them, use ``` (instead of ```CEDARScript).
If you don't want to send a CEDARScript block, you HAVE to end the message with the special tag <NOCEDARSCRIPT/> as the last line.
{shell_cmd_reminder}
"""

    example_messages = CEDARScriptPromptsBase.example_messages + [
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
UPDATE FUNCTION "myFirstFunction"
  FROM FILE "/dev/stdin"
MOVE WHOLE
INSERT BEFORE CLASS "MyClass"
  RELATIVE INDENTATION 0; -- the function being moved will start at the same indentation as the class `MyClass`

-- 2. Update the copied function to remove references to `self`, now declaring `instance_var_1` as parameter
UPDATE FUNCTION "myFirstFunction"
  FROM FILE "/dev/stdin"
REPLACE SEGMENT
    STARTING AFTER LINE "def myFirstFunction("
    ENDING AT LINE "self, name: str,"
WITH CONTENT '''
@1:instance_var_1: str, name: str,
''';
UPDATE FUNCTION "myFirstFunction"
FROM FILE "/dev/stdin"
REPLACE SEGMENT
  STARTING AFTER LINE "a = doSomething(name, age)"
  ENDING AT LINE "return a + 5 + len(self.instance_var_1) * 7"
-- `@-1:` is used because the return statement is 1 indent level to the *left* of 'a = doSomething(name, age)' (STARTING reference mark)
WITH CONTENT '''
@-1:return a + 5 + len(instance_var_1) * 7
''';

-- 3. Update ALL call sites of the method `myFirstFunction` to call the new top-level function with the same name, passing `instance_var_1` as argument
UPDATE FILE "/dev/stdin"
REPLACE SEGMENT
  STARTING AFTER LINE "def anotherFunction(self, name: str, age: int):"
  ENDING BEFORE LINE '''c = "x" + '"' + "'" + "z"''' -- multi-line string used to avoid escaping `'` and `"`
WITH CONTENT '''
@1:b = checkVal(45, "strict", myFirstFunction(instance_var_1, name, age), 8, "tops")
@1:bb = checkVal(7, "lax", myFirstFunction(instance_var_1, name, age), 2, "bottom")
''';
UPDATE FILE "/dev/stdin"
REPLACE LINE 'd = checkVal(45, "strict", self.myFirstFunction(name, age), 8, "tops")'
WITH CONTENT '''
@0:d = checkVal(45, "strict", myFirstFunction(instance_var_1, name, age), 8, "tops")
''';
UPDATE FILE "/dev/stdin"
REPLACE SEGMENT
  STARTING AT LINE \"\"\"'9"f', "as'df", self.myFirstFunction(name, age))\"\"\" -- multi-line string used to avoid escaping `'` and `"`
  ENDING BEFORE LINE 'return b * 3'
WITH CONTENT '''
@0:'9"f', "as'df", myFirstFunction(instance_var_1, name, age))
''';
{fence[1]}

Notes:
1. As the code to be changed was provided in your message, we're using file name "/dev/stdin".
2. The line "class MyClass():" was used as the insertion reference to reduce any chances of failing to apply the changes.
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
UPDATE FUNCTION "myFirstFunction"
  FROM FILE "/dev/stdin"
MOVE WHOLE
INSERT BEFORE CLASS "MyClass"
  RELATIVE INDENTATION 0; -- the block of code being moved wil start at the same indentation as the 'reference mark'

-- 2. Update the copied function to remove references to `self`, now declaring `instance_var_1` as parameter
UPDATE FUNCTION "myFirstFunction"
FROM FILE "/dev/stdin"
REPLACE SEGMENT
  STARTING AT LINE "def myFirstFunction(self, name: str, age: int):"
  ENDING BEFORE LINE '\"\"\"Lorem ipsum dolor sit amet' -- Chose the first line below the starting line to get the shortest segment possible
WITH CONTENT '''
@0:def myFirstFunction(instance_var_1: str, name: str, age: int):
''';
UPDATE FUNCTION "myFirstFunction"
  FROM FILE "/dev/stdin"
REPLACE SEGMENT
  STARTING AFTER LINE "a = doSomething(name, age)"
  ENDING AT LINE "return a + 5 + len(self.instance_var_1) * 7"
WITH CONTENT '''
@-1:return a + 5 + len(instance_var_1) * 7
''';

-- 3. Update ALL call sites of the method `myFirstFunction` to call the new top-level function with the same name, passing `instance_var_1` as argument
UPDATE FILE "/dev/stdin"
REPLACE SEGMENT
  STARTING AFTER LINE "# Check and store in 'b' and 'bb'"
  ENDING BEFORE LINE "return b + bb"
WITH CONTENT '''
@0:b = checkVal(45, "strict", myFirstFunction(instance_var_1, name, age), 8, "tops")
@0:bb = checkVal(7, "lax", myFirstFunction(instance_var_1, name, age), 2, "bottom")
''';
{fence[1]}

Notes:
1. As the code to be changed was provided in your message, we're using file name "/dev/stdin".
2. The line "class MyClass():" was used as the insertion reference to reduce any chances of failing to apply the changes.
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
REPLACE FUNCTION "__init__" -- Replace the entire function, as there's nothing to keep
WITH CONTENT '''
@0:def __init__(self):
@1:self.greeting_count: int = 0
''';

-- 2. Implement the `print_with_prefix()` method to print parameter `name` prefixed with the `prefix` parameter;
UPDATE CLASS "Greeter" -- As method `print_with_prefix` exists in more than 1 class, we specify which one we want to reference
  FROM FILE "/dev/stdin"
REPLACE FUNCTION "print_with_prefix" -- no need to preserve it, so we replace it
WITH CONTENT '''
@0:def print_with_prefix(self, prefix: str, name: str):
@1:print(f"{{prefix}}{{name}}")
''';

-- 3. Insert a call to the `print_with_prefix()` method at the top of the last method (`greet`);
UPDATE CLASS "Greeter" -- As method `greet` exists in more than 1 class, we specify which one we want to reference
  FROM FILE "/dev/stdin"
INSERT INSIDE FUNCTION "greet" TOP -- at the TOP of the function body
-- The function body is the reference indent level; `@0:` means to use that same level 
WITH CONTENT '''
@0:print_with_prefix('Hi, ', name)
''';

-- 4. Insert code at the bottom of the `greet()` method to increment the greeting count and print it.
UPDATE CLASS "Greeter" -- As method `greet` exists in more than 1 class, we specify which one we want to reference
  FROM FILE "/dev/stdin"
INSERT INSIDE FUNCTION "greet" BOTTOM -- at the BOTTOM of the function body
-- The function body is the reference indent level; `@0:` means to use that same level 
WITH CONTENT '''
@0:self.greeting_count += 1
@0:print(f'There have been {{self.greeting_count}} greetings so far.')
''';
{fence[1]}

Notes to self:
1. As the code to be changed was provided in the message, we're using file name "/dev/stdin".
2. When using `INSIDE`, the body of the function or class is implicit, so we can NEVER write `BODY` after `INSIDE`.
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
MOVE FUNCTION "calc1"
INSERT BEFORE CLASS "A"
  RELATIVE INDENTATION 0;

-- 2. Update the copied function to remove references to `self`, now declaring `instance_var` as parameter
UPDATE FUNCTION "calc1" OFFSET 1 -- Now, `calc1` exists as a top-level function before class `A` (we just moved it), but there's also a method with the same name inside class `A0`, so we use `OFFSET 1` to skip the first match (the one from `A0`)
  FROM FILE "/dev/stdin"
REPLACE LINE "def calc1(self, a):"
WITH CONTENT '''
@0:def calc1(instance_var: int, a):
''';
UPDATE FUNCTION "calc1" OFFSET 1 -- to skip 1 match (the one from `A0`)
  FROM FILE "/dev/stdin"
REPLACE LINE "after 'self') by a value stored in 'self.instance_var'."
WITH CONTENT '''
@0:after 'instance_var') by a value stored in 'instance_var'.
''';
UPDATE FUNCTION "calc1" OFFSET 1 -- to skip 1 match (the one from `A0`)
  FROM FILE "/dev/stdin"
REPLACE LINE 'return a * self.instance_var'
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
MOVE FUNCTION "calc1"
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
UPDATE FUNCTION "calc2" OFFSET 1 -- There are 2 `calc2` methods. We skip 1, meaning we target the second one (which is the one in the `A` class)
  FROM FILE "/dev/stdin"
REPLACE SEGMENT
  STARTING AFTER LINE '# Call calc1...' -- We cannot use line 'c = ["x", str(self.calc1(' as reference marker because there are 2 or more matches for it
  ENDING BEFORE LINE '5), "xx"]' -- We cannot use line 'c = ["x", str(self.calc1(' as reference marker because there are 2 or more matches for it
WITH CONTENT '''
@0:c = ["x", str(calc1(self.instance_var,
''';
UPDATE FUNCTION "calc2" OFFSET 1
  FROM FILE "/dev/stdin"
REPLACE SEGMENT
  STARTING AFTER LINE '5), "xx"]'
  ENDING BEFORE LINE '6), "xx"]'
WITH CONTENT '''
@-1:c = ["x", str(calc1(self.instance_var,
'''; -- Above, we used relative indent level -1 because the line to be replaced is 1 level to the *LEFT* of '5), "xx"]' (the starting reference line)
-- Note to self: A line marker referencing 'c = ["x", str(self.calc1(' would be ambiguous, since there are 2 or more matches for it. Thus, it's important to use another nearby line marker as reference.

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
UPDATE FILE "/dev/stdin"
REPLACE LINE "def calc2(a):"
WITH CONTENT'''
@0:def calc2(a, base_tax: float = 1.3):
''';

-- 3. Update ALL call sites of `calc1()` to pass `base_tax` as the first argument
UPDATE FILE "/dev/stdin"
REPLACE SEGMENT
  STARTING AFTER LINE 'def calc2(a, base_tax: float = 1.3):' -- We cannot use line 'c = ["x", str(calc1(' as reference marker because there are 2 or more matches for it
  ENDING BEFORE LINE '5), "xx"]' -- We cannot use line 'c = ["x", str(calc1(' as reference marker because there are 2 or more matches for it
WITH CONTENT '''
@1:c = ["x", str(calc1(base_tax,
'''; -- Above, we used relative indent level 1 because the line to be replaced is 1 level to the *RIGHT* of 'def calc2(a, base_tax: float = 1.3):' (the starting reference line)
UPDATE FUNCTION "calc2"
  FROM FILE "/dev/stdin"
REPLACE SEGMENT
  STARTING AFTER LINE '5), "xx"]'
  ENDING BEFORE LINE '6), "xx"]'
WITH CONTENT '''
@-1:c = ["x", str(calc1(base_tax,
'''; -- Above, we used relative indent level -1 because the line to be replaced is 1 level to the *LEFT* of '5), "xx"]' (the starting reference line)
-- Note to self: A line marker referencing 'c = ["x", str(calc1(' would be ambiguous, since there are 2 or more matches for it. Thus, it's important to use another nearby line marker as reference.
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
UPDATE FUNCTION "_candidate" -- As method `_candidate` only exists in one place, it's unambiguous, so we ought to directly reference it (by using `UPDATE FUNCTION..MOVE WHOLE`).
  FROM FILE "/dev/stdin"
MOVE WHOLE
INSERT BEFORE CLASS "A"
  RELATIVE INDENTATION 0;

-- 2. Update the copied function to remove references to `self`
UPDATE FUNCTION "_candidate"
  FROM FILE "/dev/stdin"
REPLACE LINE "def _candidate(self, a, b, c):"
WITH CONTENT '''
@0:def _candidate(a, b, c):
''';

-- 3. Update ALL call sites of the method `_candidate()` to call the new top-level function with the same name
UPDATE FUNCTION "_check"
  FROM FILE "/dev/stdin"
REPLACE LINE 'self._candidate(' -- There's only 1 call site and this line marker is unambiguous, so it's more concise to just replace a LINE instead of a SEGMENT
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
MOVE FUNCTION "_candidate"
INSERT BEFORE CLASS "A"
  RELATIVE INDENTATION 0;

-- 2. Update the copied function to remove references to `self`
UPDATE FUNCTION "_candidate"
  FROM FILE "/dev/stdin"
REPLACE LINE "def _candidate(self, a, b, c):"
WITH CONTENT '''
@0:def _candidate(a, b, c):
''';

-- 3. Update ALL call sites of the method `_candidate()` to call the new top-level function with the same name
UPDATE FUNCTION "_check"
  FROM FILE "/dev/stdin"
REPLACE LINE 'self._candidate(' -- There's only 1 call site and this line marker is unambiguous, so it's more concise to just replace a LINE instead of a SEGMENT
WITH CONTENT '''
@0:_candidate(
''';
{fence[1]}""",
        ),
    ]
