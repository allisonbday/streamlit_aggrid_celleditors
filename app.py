# IMPORTS ---------------------------------------------------------------------
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
from st_aggrid import GridUpdateMode, DataReturnMode

# HEADER / SETUP --------------------------------------------------------------
st.set_page_config(page_title="Ag-grid CellEditors")

st.title("Ag-grid CellEditors")
st.caption("By Allison Day")

# BODY ########################################################################

# gen dataframe
data = {
    "text": ["Lorem ipsum", "Cicero", "Werther", "Kafka", "Pangram", "Far far away"],
    "large_text": [
        "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec qu",
        "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta",
        "A wonderful serenity has taken possession of my entire soul, like these sweet mornings of spring which I enjoy with my whole heart. I am alone, and feel the charm of existence in this spot, which was",
        "One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could se",
        "The quick, brown fox jumps over a lazy dog. DJs flock by when MTV ax quiz prog. Junk MTV quiz graced by fox whelps. Bawds jog, flick quartz, vex nymphs. Waltz, bad nymph, for quick jigs vex! Fox nymph",
        "Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large",
    ],
    "select": ["Latin", "Latin", "English", "English", "English", "English"],
    "rich_select": ["Latin", "Latin", "English", "English", "English", "English"],
    "integer": [200, 26, 45, 85, 45, 123],
    "floats": [12.2, 564.5, 87.54, 321.9, 45.1, 87.9],
}
df = pd.DataFrame(data)

# datafault
st.header("Default Dataframe")
st.write(
    "Not interactive. Great for displaying information, but what if you want to edit it?"
)
st.dataframe(df)

# Aggrid ----------------------------------------------------------------------
st.write("Enter: Ag-grid")
st.header("What is Aggrid?")
st.markdown(
    """
    Aggrid is a frontend way of displaying tables in an easy to read (and edit) format! You can use it for all sorts of things. 
    Some of the more popular uses are adding checkboxes to rows, adding inline filters, and editing data!

    **Some great resources!**
    - [ag-grid documentation](https://www.ag-grid.com/)
    - [streamlit-aggrid documentation](https://streamlit-aggrid.readthedocs.io/en/docs/AgGrid.html)
    - [streamlit-aggrid examples](https://pablocfonseca-streamlit-aggrid-examples-example-jyosi3.streamlit.app/)
    """
)

# basic Ag-grid ---------------------------------------------------------------
st.header("Provided Cell Editors")
st.markdown(
    """
    Ag-grid comes with 4 [cell editors](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#select-cell-editor):
    
    1. [Text Cell Editor](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#text-cell-editor) *default* [text, integer, floats]
    2. [Large Text Cell Editor](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#large-text-cell-editor) [large_text]
    3. [Select Cell Editor](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#select-cell-editor) [select]
    4. [Rich Select Cell Editor *(AG Grid Enterprise Only)*](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#rich-select-cell-editor) [rich_select]
    """
)

gb_basic = GridOptionsBuilder.from_dataframe(df)

# default is Text Cell Editor
gb_basic.configure_columns(
    ["text", "large_text", "select", "rich_select", "integer", "floats"], editable=True
)
# cellEditor: Large Text Cell Editor
gb_basic.configure_column(
    "large_text",
    maxWidth=250,
    cellEditor="agLargeTextCellEditor",
    cellEditorPopup=True,
)
# cellEditor: Select Cell Editor
gb_basic.configure_column(
    "select",
    cellEditor="agSelectCellEditor",
    cellEditorParams={"values": ["Latin", "English"]},
    cellEditorPopup=True,
)
# cellEditor: Select Cell Editor
gb_basic.configure_column(
    "rich_select",
    cellEditor="agRichSelectCellEditor",
    cellEditorParams={
        "values": ["Latin", "English"],
        "cellHeight": 20,
    },
    cellEditorPopup=True,
)

go_basic = gb_basic.build()
grid_basic = AgGrid(
    df,
    gridOptions=go_basic,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    reload_data=False,
    enable_enterprise_modules=True,
)

with st.expander("code"):
    st.code(
        """
gb_basic = GridOptionsBuilder.from_dataframe(df)

# default is Text Cell Editor
gb_basic.configure_columns(
    ["text", "large_text", "select", "rich_select", "integer", "floats"], editable=True
)
# cellEditor: Large Text Cell Editor
gb_basic.configure_column(
    "large_text",
    maxWidth=250,
    cellEditor="agLargeTextCellEditor",
    cellEditorPopup=True,
)
# cellEditor: Select Cell Editor
gb_basic.configure_column(
    "select",
    cellEditor="agSelectCellEditor",
    cellEditorParams={"values": ["Latin", "English"]},
    cellEditorPopup=True,
)
# cellEditor: Select Cell Editor
gb_basic.configure_column(
    "rich_select",
    cellEditor="agRichSelectCellEditor",
    cellEditorParams={
        "values": ["Latin", "English"],
        "cellHeight": 20,
    },
    cellEditorPopup=True,
)

go_basic = gb_basic.build()
grid_basic = AgGrid(
    df,
    gridOptions=go_basic,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    reload_data=False,
    enable_enterprise_modules=True,
)"""
    )

st.write(
    "Notice how you can put anything in the integer and floats column, not just numbers. How can we limit it?"
)


# Custom ----------------------------------------------------------------------
st.header("Custom Cell Editors")
st.write(
    """
    You can also make custom cell editors. Here is the [documentation](https://www.ag-grid.com/javascript-data-grid/component-cell-editor/)
    
    We will be using the **Numberic** filter from this [example](https://www.ag-grid.com/javascript-data-grid/component-cell-editor/#simple-cell-editor-example). 
    """
)

st.subheader("NumbericEditor [integer]")
NumericEditor = """
    class NumericEditor {
  // gets called once before the renderer is used
  init(params) {
    // create the cell
    this.eInput = document.createElement('input');

    if (this.isCharNumeric(params.charPress)) {
      this.eInput.value = params.charPress;
    } else {
      if (params.value !== undefined && params.value !== null) {
        this.eInput.value = params.value;
      }
    }

    this.eInput.addEventListener('keypress', (event) => {
      if (!this.isKeyPressedNumeric(event)) {
        this.eInput.focus();
        if (event.preventDefault) event.preventDefault();
      } else if (this.isKeyPressedNavigation(event)) {
        event.stopPropagation();
      }
    });

    // only start edit if key pressed is a number, not a letter
    const charPressIsNotANumber =
      params.charPress && '1234567890'.indexOf(params.charPress) < 0;
    this.cancelBeforeStart = !!charPressIsNotANumber;
  }

  isKeyPressedNavigation(event) {
    return event.key === 'ArrowLeft' || event.key === 'ArrowRight';
  }

  // gets called once when grid ready to insert the element
  getGui() {
    return this.eInput;
  }

  // focus and select can be done after the gui is attached
  afterGuiAttached() {
    this.eInput.focus();
  }

  // returns the new value after editing
  isCancelBeforeStart() {
    return this.cancelBeforeStart;
  }

  // returns the new value after editing
  getValue() {
    return this.eInput.value;
  }

  isCharNumeric(charStr) {
    return charStr && !!/\d/.test(charStr);
  }

  isKeyPressedNumeric(event) {
    const charStr = event.key;
    return this.isCharNumeric(charStr);
  }
}"""

NumericEditor_codeexample = 'NumericEditor = JsCode("""' + NumericEditor + '""")'
NumericEditor_jscode = JsCode(NumericEditor)
st.code(NumericEditor_codeexample, language="js")
st.write("But this only lets you input integers. That means no periods, no floats.")


st.subheader("FloatEditor [floats]")
st.write(
    """
    **CHANGES**: 
    - in `isCharNumeric` made the regex an | statement to also include periods
    - in `getValue` , added `parseFloat(this.eInput.value).toFixed(2)` so float has 2 decimals
    """
)

FloatEditor = """
class FloatEditor {
  // gets called once before the renderer is used
  init(params) {
    // create the cell
    this.eInput = document.createElement('input');

    if (this.isCharNumeric(params.charPress)) {
      this.eInput.value = params.charPress;
    } else {
      if (params.value !== undefined && params.value !== null) {
        this.eInput.value = params.value;
      }
    }

    this.eInput.addEventListener('keypress', (event) => {
      if (!this.isKeyPressedNumeric(event)) {
        this.eInput.focus();
        if (event.preventDefault) event.preventDefault();
      } else if (this.isKeyPressedNavigation(event)) {
        event.stopPropagation();
      }
    });

    // only start edit if key pressed is a number, not a letter
    const charPressIsNotANumber =
      params.charPress && '1234567890'.indexOf(params.charPress) < 0;
    this.cancelBeforeStart = !!charPressIsNotANumber;
  }

  isKeyPressedNavigation(event) {
    return event.key === 'ArrowLeft' || event.key === 'ArrowRight';
  }

  // gets called once when grid ready to insert the element
  getGui() {
    return this.eInput;
  }

  // focus and select can be done after the gui is attached
  afterGuiAttached() {
    this.eInput.focus();
  }

  // returns the new value after editing
  isCancelBeforeStart() {
    return this.cancelBeforeStart;
  }

  // returns the new value after editing
  getValue() {
    return parseFloat(this.eInput.value).toFixed(2);
  }

  // any cleanup we need to be done here
  destroy() {
    // but this example is simple, no cleanup, we could  even leave this method out as it's optional
  }

  // if true, then this editor will appear in a popup
  isPopup() {
    // and we could leave this method out also, false is the default
    return false;
  }

  isCharNumeric(charStr) {
    return charStr && !!/(\d|.)/.test(charStr);
  }

  isKeyPressedNumeric(event) {
    const charStr = event.key;
    return this.isCharNumeric(charStr);
  }
}
"""
FloatEditor_codeexample = 'NumericEditor = JsCode("""' + FloatEditor + '""")'
FloatEditor_jscode = JsCode(FloatEditor)
st.code(FloatEditor_codeexample, language="js")


st.subheader("Results: ")
st.write("*NOTE: edited boxes now turn green!*")


gb_custom = GridOptionsBuilder.from_dataframe(df)
# default is Text Cell Editor
gb_custom.configure_columns(
    ["text", "large_text", "select", "rich_select", "integer", "floats"], editable=True
)
# cellEditor: Large Text Cell Editor
gb_custom.configure_column(
    "large_text",
    maxWidth=250,
    cellEditor="agLargeTextCellEditor",
    cellEditorPopup=True,
)
# cellEditor: Select Cell Editor
gb_custom.configure_column(
    "select",
    cellEditor="agSelectCellEditor",
    cellEditorParams={"values": ["Latin", "English"]},
    cellEditorPopup=True,
)
# cellEditor: Select Cell Editor
gb_custom.configure_column(
    "rich_select",
    cellEditor="agRichSelectCellEditor",
    cellEditorParams={
        "values": ["Latin", "English"],
        "cellHeight": 20,
    },
    cellEditorPopup=True,
)
# CUSTOM cellEditor: NumericEditor
gb_custom.configure_column(
    "integer",
    editable=True,
    cellEditor=NumericEditor_jscode,
    cellEditorPopup=True,
)
# CUSTOM cellEditor: NumericEditor
gb_custom.configure_column(
    "floats",
    editable=True,
    cellEditor=FloatEditor_jscode,
    cellEditorPopup=True,
)

js = JsCode(
    """
function(e) {
    let api = e.api;
    let rowIndex = e.rowIndex;
    let col = e.column.colId;

    let rowNode = api.getDisplayedRowAtIndex(rowIndex);
    api.flashCells({
      rowNodes: [rowNode],
      columns: [col],
      flashDelay: 10000000000000000
    });

};
"""
)
gb_custom.configure_grid_options(onCellValueChanged=js)
go_custom = gb_custom.build()
grid_custom = AgGrid(
    df,
    gridOptions=go_custom,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    reload_data=False,
    enable_enterprise_modules=True,
    allow_unsafe_jscode=True,
)

with st.expander("code"):
    st.code(
        'js = JsCode("""'
        """
function(e) {
    let api = e.api;
    let rowIndex = e.rowIndex;
    let col = e.column.colId;

    let rowNode = api.getDisplayedRowAtIndex(rowIndex);
    api.flashCells({
      rowNodes: [rowNode],
      columns: [col],
      flashDelay: 10000000000000000
    });

};
"""
        + '"""\n'
        + """gb_custom = GridOptionsBuilder.from_dataframe(df)
    # default is Text Cell Editor
    gb_custom.configure_columns(
        ["text", "large_text", "select", "rich_select", "integer", "floats"], editable=True
    )
    # cellEditor: Large Text Cell Editor
    gb_custom.configure_column(
        "large_text",
        maxWidth=250,
        cellEditor="agLargeTextCellEditor",
        cellEditorPopup=True,
    )
    # cellEditor: Select Cell Editor
    gb_custom.configure_column(
        "select",
        cellEditor="agSelectCellEditor",
        cellEditorParams={"values": ["Latin", "English"]},
        cellEditorPopup=True,
    )
    # cellEditor: Select Cell Editor
    gb_custom.configure_column(
        "rich_select",
        cellEditor="agRichSelectCellEditor",
        cellEditorParams={
            "values": ["Latin", "English"],
            "cellHeight": 20,
        },
        cellEditorPopup=True,
    )
    # CUSTOM cellEditor: NumericEditor
    gb_custom.configure_column(
        "integer",
        editable=True,
        cellEditor=NumericEditor_jscode,
        cellEditorPopup=True,
    )
    # CUSTOM cellEditor: NumericEditor
    gb_custom.configure_column(
        "floats",
        editable=True,
        cellEditor=FloatEditor_jscode,
        cellEditorPopup=True,
    )

    )
    gb_custom.configure_grid_options(onCellValueChanged=js)
    go_custom = gb_custom.build()
    grid_custom = AgGrid(
        df,
        gridOptions=go_custom,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        reload_data=False,
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True,
    )"""
    )


st.write("**Data Out:**")
st.dataframe(grid_custom["data"])
