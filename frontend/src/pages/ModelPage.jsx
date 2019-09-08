import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

import Container from 'react-bootstrap/Container';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBackward } from "@fortawesome/free-solid-svg-icons";

import Loading from "./components/Loading";

import Pentagon from "./components/Pentagon";

import {REMOTE_SERVER} from '../config.js';


export default class ModelPage extends Component {
  constructor(props){
    super(props);
    this.state = {
      model : {},
      loaded : false
    }
  }

  componentWillMount(){
    const model_id = this.props.match.params.id;

    axios.get(REMOTE_SERVER+'/ajax/get_model/'+model_id)
    .then(res => {
      if (res.status == 200){
        this.setState({model : res.data.model, loaded : true});
      }
    });
  }

  render(){
    if (this.state.loaded){
      return(
        <Container>
          <Card>
            <Card.Header>
              <Link to="/browse/models"><FontAwesomeIcon icon={faBackward}/></Link>
              <Card.Title>{this.state.model.name}</Card.Title>
              <Card.Subtitle>{this.state.model.desc}</Card.Subtitle>
            </Card.Header>
            <Card.Body>
              <h4>Fill this please</h4>
            </Card.Body>
          </Card>
        </Container>
      );
    }else{
      return(
        <Loading text="Loading model..."/>
      );
    }
  }
}
