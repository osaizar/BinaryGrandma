import React, { Component } from 'react';

import Container from 'react-bootstrap/Container';

import pentagon from "./pentagon.js";


export default class Pentagon extends Component {
  constructor(props){
    super(props);
  }

  componentDidMount(){
    pentagon(this.props.results);
  }

  render(){
    return(
      <Container className="container-canvas-main">
        <div className="container-canvas">
          <canvas id="pentagonCanvas" width="800px" height="450px"></canvas>
        </div>
      </Container>
    );
  }
}
