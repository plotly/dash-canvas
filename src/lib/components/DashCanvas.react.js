import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {SketchField, Tools} from 'react-sketch';


/**
 * A canvas component for drawing on a background image and selecting
 * regions.
 */
export default class DashCanvas extends Component {
    constructor(props) {
    super(props);
    this.state = {
    };
    this._save = this._save.bind(this);
    this._undo = this._undo.bind(this);
  } 


    componentDidMount() {
    if (this.props.filename.length > 0){
	let sketch = this._sketch;
	let opts = {left:0,
		    top:0,
		    scale:this.props.scale}
	sketch.addImg(this.props.filename, opts);
	}
    if (this.props.image_content.length > 0){
	let sketch = this._sketch;
	let opts = {left:0,
		    top:0,
		    scale:this.props.scale}
	sketch.addImg(this.props.image_content, opts);
	}

    }

    componentDidUpdate(prevProps) {
    let sketch = this._sketch;
    // Typical usage (don't forget to compare props):
    if ( 
	(this.props.image_content !== prevProps.image_content)){
	sketch.clear();
	this.props.setProps({json_data: ''});
	let opts = {left:0,
		    top:0,
		    scale:this.props.scale}
	sketch.addImg(this.props.image_content, opts);
    };


    };

    _save() {
        let JSON_string = JSON.stringify(this._sketch.toJSON());
	let toggle_value = this.props.trigger + 1
	this.props.setProps({json_data: JSON_string, trigger: toggle_value});
    };


    _undo(){
        this._sketch.undo();
        this.setState({
            canUndo: this._sketch.canUndo(),
            canRedo: this._sketch.canRedo()
        })
    };


    render() {
	let value;
      if (this.props.setProps) {
        value = this.props.value;
      } else {
        value = this.state.value;
      }
      var toolsArray = {};
      toolsArray["pencil"] = Tools.Pencil;
      toolsArray["pan"] = Tools.Pan;
      toolsArray["circle"] = Tools.Circle;
        return (
		<div className={this.props.className}>
	    	<SketchField name='sketch'
                         ref={(c) => this._sketch = c}
                         tool={toolsArray[this.props.tool.toLowerCase()]}
                         lineColor={this.props.lineColor}
			 width={this.props.width}
			 height={this.props.height}
                         lineWidth={this.props.lineWidth}/>
		       <button onClick={(e) => this._undo()}> Undo </button>
		       <button onClick={(e) => this._sketch.zoom(1.25)}> Zoom </button>
		       <button onClick={(e) => this._sketch.zoom(0.8)}> Unzoom </button>
		       <button onClick={(e) => this._save()}> Save </button>
		</div>
	    

        )
     }


}

DashCanvas.defaultProps = {filename:'', 
			   json_data:'', image_content:'', trigger:0,
			   width:500, height:500, scale:1, lineWidth:20,
			   lineColor:'yellow', tool:"pencil"};

DashCanvas.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks
     */
    id: PropTypes.string,

    /**
     * className of the parent div
     */
    className: PropTypes.string,

    /**
     * A label that will be printed when this component is rendered.
     */
    label: PropTypes.string.isRequired,

    /**
     * Image data
     */
    image_content: PropTypes.string,
 
    /**
     * The width of the canvas
     */
    width: PropTypes.number,
 
     /**
     * The height of the canvas
     */
    height: PropTypes.number,

    /**
     * Scaling factor of image
     */
    scale: PropTypes.number,
 
    /**
     * Selection or drawing tool
     */
    tool: PropTypes.string,
 
    /**
     * Width of drawing line
     */
    lineWidth: PropTypes.number,

    /**
     * Color of drawing line
     */
    lineColor: PropTypes.string,

    /**
     * Name of image file to load
     */
    filename: PropTypes.string,

    /**
     * Bla
     */
    trigger: PropTypes.number,
    
    /**
     * Sketch content as JSON string
     */
    json_data: PropTypes.string,
    
    /**
     * Dash-assigned callback that should be called whenever any of the
     * properties change
     */
    setProps: PropTypes.func
};
