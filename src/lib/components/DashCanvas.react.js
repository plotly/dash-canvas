import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {SketchField, Tools} from 'react-sketch';
import DropZone from 'react-dropzone';


/**
 * DashCanvas is an example component.
 */
export default class DashCanvas extends Component {
    constructor(props) {
    super(props);
    this.state = {
        lineColor: 'black',
        lineWidth: 30,
        fillColor: '#68CCCA',
        backgroundColor: 'transparent',
        shadowWidth: 0,
        shadowOffset: 0,
        tool: Tools.Line,
        fillWithColor: false,
        fillWithBackgroundColor: false,
        drawings: [],
        canUndo: false,
        canRedo: false,
        controlledSize: false,
        sketchWidth: 600,
        sketchHeight: 600,
        stretched: false,
        stretchedX: false,
        stretchedY: false,
        originX: 'left',
        originY: 'top'
    };
    this._save = this._save.bind(this);
    this._undo = this._undo.bind(this);
    this._resize = this._resize.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
  } 


    componentDidMount() {
    let sketch = this._sketch;
    sketch.setBackgroundFromDataUrl(this.props.filename, {});
    }

    componentDidUpdate(prevProps) {
    let sketch = this._sketch;
    // Typical usage (don't forget to compare props):
    if (this.props.image_content !== prevProps.image_content) {
        let {stretched, stretchedX, stretchedY, originX, originY} = this.state;
        sketch.setBackgroundFromDataUrl(this.props.image_content, {
                stretched: stretched,
                stretchedX: stretchedX,
                stretchedY: stretchedY,
                originX: originX,
                originY: originY
            });
       }
      let JSON_content = JSON.stringify(this._sketch.toJSON());
      console.log(JSON_content);
    };

    _save() {
        let JSON_string = JSON.stringify(this._sketch.toJSON());
	this.props.setProps({json_data: JSON_string});
    };


    _addImg() {
	let sketch = this._sketch;
        let {stretched, stretchedX, stretchedY, originX, originY} = this.state;
        sketch.setBackgroundFromDataUrl(this.props.filename, {
                stretched: stretched,
                stretchedX: stretchedX,
                stretchedY: stretchedY,
                originX: originX,
                originY: originY
            });

    };

    _resize(e) {
    this.setState({controlledSize: !this.state.controlledSize});
    };


    _undo(){
        this._sketch.undo();
        this.setState({
            canUndo: this._sketch.canUndo(),
            canRedo: this._sketch.canRedo()
        })
    };


    handleInputChange(e) {
      const newValue = e.target.value;
      this.props.setProps({value: newValue});
      this._sketch.setProps({lineColor: 'green'});
    };

    render() {
	let value;
      if (this.props.setProps) {
        value = this.props.value;
      } else {
        value = this.state.value;
      }
        return (
		<div>
	   	<h1> Oh Oh </h1>
	    	<SketchField name='sketch'
                         ref={(c) => this._sketch = c}
                         tool={Tools.Pencil}
                         lineColor={this.props.lineColor}
			 width={this.props.width}
			 height={this.props.height}
                         lineWidth={this.state.lineWidth}/>
			<button 
		       onClick={(e, v) => this._resize(e, v)}> Resize </button>
			<button 
		       onClick={(e) => this._undo()}> Undo </button>
			<button
		       onClick={(e) => this._addImg()}> Image </button>
			<button
		       onClick={(e) => this._save()}> Save </button>
		</div>
	    

        )
     }


}

DashCanvas.defaultProps = {filename:'camera.png', value:'bla', 
			   json_data:'', image_content:'',
			   width:500, height:500};

DashCanvas.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks
     */
    id: PropTypes.string,

    /**
     * A label that will be printed when this component is rendered.
     */
    label: PropTypes.string.isRequired,

    /**
     * The value displayed in the input
     */
    value: PropTypes.string,
    /**
     * the color of the line
     */
    lineColor: PropTypes.string,

    /**
     * The value displayed in the input
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
     * The value displayed in the input
     */
    filename: PropTypes.string,
    
    /**
     * The value displayed in the input
     */
    json_data: PropTypes.string,
    
    /**
     * Dash-assigned callback that should be called whenever any of the
     * properties change
     */
    setProps: PropTypes.func
};
