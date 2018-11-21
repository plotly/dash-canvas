import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {SketchField, Tools} from 'react-sketch';
import DropZone from 'react-dropzone';
// import SaveIcon from 'material-ui/svg-icons/content/save';
// import Slider from 'material-ui';
// import getMuiTheme from 'material-ui/styles/getMuiTheme';
// import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';


/**
 * DashCanvas is an example component.
 * It takes a property, `label`, and
 * displays it.
 * It renders an input with the property `value`
 * which is editable by the user.
 */
export default class DashCanvas extends Component {
    constructor(props) {
    super(props);
    this.state = {
        lineColor: 'black',
        lineWidth: 10,
        fillColor: '#68CCCA',
        backgroundColor: 'transparent',
        shadowWidth: 0,
        shadowOffset: 0,
        tool: Tools.Pencil,
        fillWithColor: false,
        fillWithBackgroundColor: false,
        drawings: [],
        canUndo: false,
        canRedo: false,
        controlledSize: false,
        sketchWidth: 600,
        sketchHeight: 600,
        stretched: true,
        stretchedX: false,
        stretchedY: false,
        originX: 'left',
        originY: 'top'
    };
    this._save = this._save.bind(this);
    this._onBackgroundImageDrop = this._onBackgroundImageDrop.bind(this);
    this._undo = this._undo.bind(this);
    this._resize = this._resize.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
  } 

    componentDidUpdate(prevProps) {
    // Typical usage (don't forget to compare props):
    if (this.props.image_content !== prevProps.image_content) {
  	let sketch = this._sketch;
        let {stretched, stretchedX, stretchedY, originX, originY} = this.state;
        sketch.setBackgroundFromDataUrl(this.props.image_content, {
                stretched: stretched,
                stretchedX: stretchedX,
                stretchedY: stretchedY,
                originX: originX,
                originY: originY
            });
       }
    };

    _save() {
        let content = this._sketch.toJSON();
        let JSON_string = JSON.stringify(this._sketch.toJSON());
	this.props.setProps({json_data: JSON_string});
    };


    _blo() {
    console.log("Oh Ah");
    const filename = this.props.filename
    console.log(filename);
    this._sketch.addImg(filename, opts);
    };

    _addImg() {
    let opts = {
                left: 0,
                top: 0,
                scale: 1
            };
    this._sketch.addImg(this.props.filename, opts);
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

     _onBackgroundImageDrop(accepted/*, rejected*/) {
        if (accepted && accepted.length > 0) {
            let sketch = this._sketch;
            let reader = new FileReader();
            let {stretched, stretchedX, stretchedY, originX, originY} = this.state;
            reader.addEventListener('load', () => sketch.setBackgroundFromDataUrl(reader.result, {
                stretched: stretched,
                stretchedX: stretchedX,
                stretchedY: stretchedY,
                originX: originX,
                originY: originY
            }), false);
            reader.readAsDataURL(accepted[0]);
        }
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
		 <div>
				<DropZone
				    ref="dropzone"
				    accept='image/*'
				    multiple={false}
				    onDrop={this._onBackgroundImageDrop}>
				    Try dropping an image here,<br/>
				    or click<br/>
				    to select image as background.
				</DropZone>
			    </div>

	    	<SketchField name='sketch'
                         ref={(c) => this._sketch = c}
                         width='200px'
                         height='200px'
                         tool={Tools.Pencil}
                         lineColor={this.props.lineColor}
			 width={this.state.controlledSize ? this.state.sketchWidth : null}
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
			   JSON_string:'', image_content:''};

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
     * The value displayed in the input
     */
    filename: PropTypes.string,
    
    /**
     * The value displayed in the input
     */
    JSON_string: PropTypes.string,
    
    /**
     * Dash-assigned callback that should be called whenever any of the
     * properties change
     */
    setProps: PropTypes.func
};
