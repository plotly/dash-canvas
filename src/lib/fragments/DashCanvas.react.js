import React, { Component } from 'react';
import { SketchField, Tools } from 'react-sketch';
import {
	ZoomMinusIcon, ZoomPlusIcon, EditIcon, PanIcon,
	ArrowLeftIcon, ArrowRightIcon, PlotLineIcon, SquareIcon, TagOutlineIcon
}
	from 'plotly-icons';

import { propTypes, defaultProps } from '../components/DashCanvas.react';

const styles = {
	button: {
		margin: '3px',
		padding: '0px',
		width: '50px',
		height: '50px',
		verticalAlign: 'middle',
	},

	textbutton: {
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
			height: 200,
			width: 200
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
	     this.canvasRef = React.createRef();
	}


	componentDidMount() {
		let sketch = this._sketch;
		if (this.props.width == 0) {
		    this.setState({width: this.canvasRef.current.clientWidth});
		} else{
		    this.setState({width: this.props.width});
		}

		// Control resize - does not work at the moment
		window.addEventListener('resize', this._resize, false);
		
		if (this.props.filename.length > 0 ||
			this.props.image_content.length > 0) {
			var content = (this.props.filename.length > 0) ? this.props.filename :
				this.props.image_content;
			var img = new Image();
			img.onload = () => {
				var new_height = this.state.height;
				var new_scale = 1;
				var height = img.height;
				var width = img.width;
				new_height = Math.round(height * this.state.width / width);
				new_scale = new_height / height;
				this.setState({ height: new_height });
				sketch.clear();
				let opts = {
					left: 0,
					top: 0,
					scale: new_scale
				}
				sketch.addImg(content, opts);
			}
			img.src = content;
		} else {
			sketch._fc.setBackgroundColor(sketch.props.backgroundColor);
		}
	}


	componentDidUpdate(prevProps) {
		let sketch = this._sketch;
		// Typical usage (don't forget to compare props):
		if (
			(this.props.image_content !== prevProps.image_content)) {
			var img = new Image();
			var new_height = this.state.height;
			var new_scale = 1;
			img.onload = () => {
				var height = img.height;
				var width = img.width;
				new_height = Math.round(height * sketch.state.width / width);
				new_scale = new_height / height;
				this.setState({ height: new_height });
				sketch.clear();
				let opts = {
					left: 0,
					top: 0,
					scale: new_scale
				}
				sketch.addImg(this.props.image_content, opts);
			}
			img.src = this.props.image_content;
			if (this.props.setProps) {
				let JSON_string = JSON.stringify(this._sketch.toJSON());
				this.props.setProps({ json_data: JSON_string });
			}

			sketch._fc.setZoom(this.props.zoom);
		};
	};


	_save() {
		let JSON_string = JSON.stringify(this._sketch.toJSON());
		let toggle_value = this.props.trigger + 1
		if (this.props.setProps) {
			this.props.setProps({ json_data: JSON_string, trigger: toggle_value });
		}
	};

	_resize() {
	    // not used yet
	    this.setState({width: this.canvasRef.current.clientWidth});
	};

	_undo() {
		this._sketch.undo();
		this.setState({
			canUndo: this._sketch.canUndo(),
			canRedo: this._sketch.canRedo()
		})
	};
	_redo() {
		this._sketch.redo();
		this.setState({
			canUndo: this._sketch.canUndo(),
			canRedo: this._sketch.canRedo()
		})
	};

	_zoom_factor(factor) {
		this._sketch.zoom(factor);
		let zoom_factor = this.props.zoom;
		this.props.setProps({ zoom: factor * zoom_factor })
	};


	_zoom() {
		this._sketch.zoom(1.25);
		let zoom_factor = this.props.zoom;
		this.props.setProps({ zoom: 1.25 * zoom_factor })
	};


	_unzoom() {
		this._sketch.zoom(0.8);
		let zoom_factor = this.props.zoom;
		this.props.setProps({ zoom: 0.8 * zoom_factor });
	};


	_pantool() {
		this.props.setProps({ tool: "pan" });
	};


	_penciltool() {
		this.props.setProps({ tool: "pencil" });
	};


	_linetool() {
		this.props.setProps({ tool: "line" });
	};


	_rectangletool() {
		this.props.setProps({ tool: "rectangle" });
	};



	_selecttool() {
		this.props.setProps({ tool: "select" });
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
		var width = width_defined ? this.props.width : this.state.width;
		var height_defined = this.props.height > 0;
		var height = height_defined ? this.props.height : this.state.height;
		return (
			<div className={this.props.className} ref={this.canvasRef}>
				<SketchField name='sketch'
					ref={(c) => this._sketch = c}
					tool={toolsArray[this.props.tool.toLowerCase()]}
					lineColor={this.props.lineColor}
					width={width}
					height={height}
					forceValue={true}
					backgroundColor='#ccddff'
					lineWidth={this.props.lineWidth} />
				{show_zoom &&
					<button style={styles.button}
						title="Zoom in"
						onClick={(e) => this._zoom()}>
						<ZoomPlusIcon />
					</button>
				}
				{show_zoom &&
					<button style={styles.button}
						title="Zoom out"
						onClick={(e) => this._unzoom()}>
						<ZoomMinusIcon />
					</button>
				}
				{show_pencil &&
					<button style={styles.button}
						title="Pencil tool"
						onClick={(e) => this._penciltool()}>
						<EditIcon />
					</button>
				}
				{show_line &&
					<button style={styles.button}
						title="Line tool"
						onClick={(e) => this._linetool()}>
						<PlotLineIcon />
					</button>
				}
				{show_rectangle &&
					<button style={styles.button}
						title="Rectangle tool"
						onClick={(e) => this._rectangletool()}>
						<SquareIcon />
					</button>
				}
				{show_pan &&
					<button style={styles.button}
						title="Pan"
						onClick={(e) => this._pantool()}>
						<PanIcon />
					</button>
				}
				{show_undo &&
					<button style={styles.button}
						title="Undo"
						onClick={(e) => this._undo()}>
						<ArrowLeftIcon />
					</button>
				}
				{show_undo &&
					<button style={styles.button}
						title="Redo"
						onClick={(e) => this._redo()}>
						<ArrowRightIcon />
					</button>
				}
				{show_select &&
					<button style={styles.button}
						title="Select"
						onClick={(e) => this._selecttool()}>
						<TagOutlineIcon />
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

DashCanvas.defaultProps = defaultProps;
DashCanvas.propTypes = propTypes;
