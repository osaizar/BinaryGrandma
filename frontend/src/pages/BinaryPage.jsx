import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

import Container from 'react-bootstrap/Container';
import Card from 'react-bootstrap/Card';

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBackward } from "@fortawesome/free-solid-svg-icons";

import BinaryResultsPanel from './components/BinaryResultsPanel';
import Loading from './components/Loading';

import {REMOTE_SERVER} from '../config.js';


export default class BinaryPage extends Component {
  constructor(props){
    super(props);
    this.state = {
      binary : {},
      loaded : false
    }
  }

  componentWillMount(){
    const binary_id = this.props.match.params.id;

    axios.get(REMOTE_SERVER+'/ajax/get_binary/'+binary_id)
    .then(res => {
      if (res.status == 200){
        this.setState({binary : res.data.binary, loaded : true});
      }
    });
  }

  render(){
    if (this.state.loaded){
      return(
        <Container>
          <Card>
            <Card.Header>
              <Link to="/browse/binaries"><FontAwesomeIcon icon={faBackward}/></Link>
              <Card.Title>{this.state.binary.name}</Card.Title>
              <Card.Subtitle>Hash: {this.state.binary.hash}</Card.Subtitle>
            </Card.Header>
            <Card.Body>
              <BinaryResultsPanel binary={this.state.binary}/>
            </Card.Body>
          </Card>
        </Container>
      );
    }else{
      return(
        <Loading text="Loading..."/>
      );
    }
  }
}
