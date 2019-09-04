import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {SketchField, Tools} from 'react-sketch';
import {ZoomMinusIcon, ZoomPlusIcon, EditIcon, PanIcon,
	ArrowLeftIcon, ArrowRightIcon, PlotLineIcon, SquareIcon, TagOutlineIcon}
	from 'plotly-icons';


const styles = {
    button: {
	margin: '3px',
        padding: '0px',
	width: '50px',
	height: '50px',
	verticalAlign: 'middle',
    },

    textbutton:{
	verticalAlign: 'top',
	height: '50px',
	color: 'blue',
	verticalAlign: 'middle',
	}
};

/**
 * Canvas component for drawing on a background image and selecting
 * regions.
 */
export default class DashCanvas extends Component {
    constructor(props) {
    super(props);
    this.state = {
	height:200
    };
    this._save = this._save.bind(this);
    this._undo = this._undo.bind(this);
    this._zoom = this._zoom.bind(this);
    this._zoom_factor = this._zoom_factor.bind(this);
    this._unzoom = this._unzoom.bind(this);
    this._pantool = this._pantool.bind(this);
    this._penciltool = this._penciltool.bind(this);
    this._linetool = this._linetool.bind(this);
    this._selecttool = this._selecttool.bind(this);
  } 


    componentDidMount() {
    let sketch = this._sketch;
    if (this.props.filename.length > 0 ||
	this.props.image_content.length > 0){
	var content = (this.props.filename.length > 0) ? this.props.filename :
		    this.props.image_content;
	var img = new Image();
	img.onload = () => {
	    var new_height = this.state.height;
	    var new_scale = 1;
	    var height = img.height;
	    var width = img.width;
	    new_height = Math.round(height * sketch.props.width / width);
	    new_scale = new_height / height;
	    this.setState({height:new_height});
	    sketch.clear();
	    let opts = {left:0,
			top:0,
			scale:new_scale}
	    sketch.addImg(content, opts);
	}
	img.src = content;
	} else{
    sketch._fc.setBackgroundColor(sketch.props.backgroundColor);
	}
    }


    componentDidUpdate(prevProps) {
    let sketch = this._sketch;
    // Typical usage (don't forget to compare props):
    if (
	(this.props.image_content !== prevProps.image_content)){
	var img = new Image();
	var new_height = this.state.height;
	var new_scale = 1;
	img.onload = () => {
	    var height = img.height;
	    var width = img.width;
	    new_height = Math.round(height * sketch.props.width / width);
	    new_scale = new_height / height;
	    this.setState({height:new_height});
	    sketch.clear();
	    let opts = {left:0,
			top:0,
			scale:new_scale}
	    sketch.addImg(this.props.image_content, opts);
	}
	img.src = this.props.image_content;
	if (this.props.setProps){
	    let JSON_string = JSON.stringify(this._sketch.toJSON());
	    this.props.setProps({json_data: JSON_string});
	    }

	sketch._fc.setZoom(this.props.zoom);
    };
    };


    _save() {
        let JSON_string = JSON.stringify(this._sketch.toJSON());
	let toggle_value = this.props.trigger + 1
	if (this.props.setProps){
	this.props.setProps({json_data: JSON_string, trigger: toggle_value});
	}
    };


    _undo(){
        this._sketch.undo();
        this.setState({
            canUndo: this._sketch.canUndo(),
            canRedo: this._sketch.canRedo()
        })
	};
	_redo(){
		this._sketch.redo();
		console.log(this._sketch);
        this.setState({
            canUndo: this._sketch.canUndo(),
            canRedo: this._sketch.canRedo()
        })
    };

    _zoom_factor(factor){
	this._sketch.zoom(factor);
	let zoom_factor = this.props.zoom;
	this.props.setProps({zoom: factor*zoom_factor})
    };


    _zoom(){
	this._sketch.zoom(1.25);
	let zoom_factor = this.props.zoom;
	this.props.setProps({zoom: 1.25*zoom_factor})
    };


    _unzoom(){
	this._sketch.zoom(0.8);
	let zoom_factor = this.props.zoom;
	this.props.setProps({zoom: 0.8*zoom_factor});
    };


    _pantool(){
	this.props.setProps({tool: "pan"});
	};


    _penciltool(){
	this.props.setProps({tool: "pencil"});
	};


    _linetool(){
	this.props.setProps({tool: "line"});
	};


    _rectangletool(){
	this.props.setProps({tool: "rectangle"});
	};



    _selecttool(){
	this.props.setProps({tool: "select"});
	};




    render() {
        var toolsArray = {};
        toolsArray["pencil"] = Tools.Pencil;
        toolsArray["pan"] = Tools.Pan;
        toolsArray["line"] = Tools.Line;
        toolsArray["circle"] = Tools.Circle;
        toolsArray["select"] = Tools.Select;
        toolsArray["rectangle"] = Tools.Rectangle;
	const hide_buttons = this.props.hide_buttons;
	const show_line = !(hide_buttons.includes("line"));
	const show_pan = !(hide_buttons.includes("pan"));
	const show_zoom = !(hide_buttons.includes("zoom"));
	const show_pencil = !(hide_buttons.includes("pencil"));
	const show_undo = !(hide_buttons.includes("undo"));
	const show_select = !(hide_buttons.includes("select"));
	const show_rectangle = !(hide_buttons.includes("rectangle"));
	var width_defined = this.props.width > 0;
	var width = width_defined ? this.props.width : null;
        return (
	    <div className={this.props.className}>
	    <SketchField name='sketch'
		ref={(c) => this._sketch = c}
                tool={toolsArray[this.props.tool.toLowerCase()]}
                lineColor={this.props.lineColor}
		width={width}
		height={this.state.height}
		forceValue={true}
		backgroundColor='#ccddff'
                lineWidth={this.props.lineWidth}/>
	    {show_zoom &&
	    <button style={styles.button}
		    title="Zoom in"
		    onClick={(e) => this._zoom()}>
		<ZoomPlusIcon/>
	    </button>
	    }
	    {show_zoom &&
	    <button style={styles.button}
		    title="Zoom out"
		    onClick={(e) => this._unzoom()}>
		<ZoomMinusIcon/>
	    </button>
	    }
	    {show_pencil &&
	    <button style={styles.button}
		    title="Pencil tool"
		    onClick={(e) => this._penciltool()}>
		<EditIcon/>
	    </button>
	    }
	    {show_line &&
	    <button style={styles.button}
		    title="Line tool"
		    onClick={(e) => this._linetool()}>
		<PlotLineIcon/>
	    </button>
	    }
	    {show_rectangle &&
	    <button style={styles.button}
		    title="Rectangle tool"
		    onClick={(e) => this._rectangletool()}>
		<SquareIcon/>
	    </button>
	    }
	    {show_pan &&
	    <button style={styles.button}
		    title="Pan"
		    onClick={(e) => this._pantool()}>
		<PanIcon/>
	    </button>
	    }
	    {show_undo &&
	    <button style={styles.button}
		    title="Undo"
		    onClick={(e) => this._undo()}>
		<ArrowLeftIcon/>
	    </button>
		}
		{show_undo &&
	    <button style={styles.button}
		    title="Redo"
		    onClick={(e) => this._redo()}>
		<ArrowRightIcon/>
	    </button>
	    }
	    {show_select &&
	    <button style={styles.button}
		    title="Select"
		    onClick={(e) => this._selecttool()}>
		<TagOutlineIcon/>
	    </button>
	    }

		<button style={styles.textbutton}
		    title="Save"
		    onClick={(e) => this._save()}>
		    {this.props.goButtonTitle}
	    </button>

	    </div>

        )
     }


}

DashCanvas.defaultProps = {filename:'',
			   json_data:'', image_content:'', trigger:0,
			   width:500, height:500, scale:1, lineWidth:10,
			   lineColor:'red', tool:"pencil", zoom:1,
			   goButtonTitle:'Save', hide_buttons:[]};

DashCanvas.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks
     */
    id: PropTypes.string,

    /**
     * Image data string, formatted as png or jpg data string. Can be
     * generated by utils.io_utils.array_to_data_string.
     */
    image_content: PropTypes.string,
 
    /**
     * Zoom factor
     */
    zoom: PropTypes.number,
 

    /**
     * Width of the canvas
     */
    width: PropTypes.number,
 
     /**
     * Height of the canvas
     */
    height: PropTypes.number,

    /**
     * Scaling ratio between canvas width and image width
     */
    scale: PropTypes.number,
 
    /**
     * Selection of drawing tool, among ["pencil", "pan", "circle",
     * "rectangle", "select", "line"].
     */
    tool: PropTypes.string,
 
    /**
     * Width of drawing line (in pencil mode)
     */
    lineWidth: PropTypes.number,

    /**
     * Color of drawing line (in pencil mode). Can be a text string,
     * like 'yellow', 'red', or a color triplet like 'rgb(255, 0, 0)'.
     * Alpha is possible with 'rgba(255, 0, 0, 0.5)'.
     */
    lineColor: PropTypes.string,

    /**
     * Title of button 
     */
    goButtonTitle: PropTypes.string,


    /**
     * Name of image file to load (URL string)
     */
    filename: PropTypes.string,


    /**
     * Counter of how many times the save button was pressed
     * (to be used mostly as input)
     */
    trigger: PropTypes.number,
    
    /**
     * Sketch content as JSON string, containing background image and
     * annotations. Use utils.parse_json.parse_jsonstring to parse
     * this string.
     */
    json_data: PropTypes.string,

    /**
     * Names of buttons to hide. Names are "zoom", "pan", "line", "pencil",
     * "rectangle", "undo", "select".
     */
    hide_buttons: PropTypes.arrayOf(PropTypes.string),
    
    /**
     * Dash-assigned callback that should be called whenever any of the
     * properties change
     */
    setProps: PropTypes.func
};
