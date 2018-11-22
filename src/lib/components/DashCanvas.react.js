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
        lineColor: 'black',
        lineWidth: 30,
        shadowWidth: 0,
        shadowOffset: 0,
        drawings: [],
        stretched: false,
        stretchedX: false,
        stretchedY: false,
        originX: 'left',
        originY: 'top'
    };
    this._save = this._save.bind(this);
    this._undo = this._undo.bind(this);
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
        return (
		<div>
	    	<SketchField name='sketch'
                         ref={(c) => this._sketch = c}
                         tool={Tools.Pencil}
                         lineColor={this.props.lineColor}
			 width={this.props.width}
			 height={this.props.height}
                         lineWidth={this.state.lineWidth}/>
		       <button onClick={(e) => this._undo()}> Undo </button>
		       <button onClick={(e) => this._save()}> Save </button>
		</div>
	    

        )
     }


}

DashCanvas.defaultProps = {filename:'camera.png', 
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
     * Name of image file to load
     */
    filename: PropTypes.string,
    
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
