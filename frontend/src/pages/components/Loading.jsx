import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

import Image from 'react-bootstrap/Image';
import Container from 'react-bootstrap/Container';

export default class Loading extends Component {
  constructor(props){
    super(props)
  }

  render(){
    return(
      <Container>
        <Image src="/img/loading.gif" fluid className="align-self-center"></Image>
        <h4>{this.props.text}</h4>
      </Container>
    );
  }
}
