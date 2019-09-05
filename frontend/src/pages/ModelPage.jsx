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

    axios.get('http://localhost:5000/ajax/get_model/'+model_id)
    .then(res => {
      if (res.status == 200){
        this.setState({model : res.data.model, loaded : true});
      }
    });
  }

  render(){
    if (this.state.loaded){
      var results = [{"name" : "model1", "value" : 34}, {"name" : "model2", "value" : 92},
                     {"name" : "model3", "value" : 54}, {"name" : "model4", "value" : 4},
                     {"name" : "model5", "value" : 12}, {"name" : "model6", "value" : 90},
                     {"name" : "model8", "value" : 98}, {"name" : "model7", "value" : 80},
                    ];
      return(
        <Container>
          <Card>
            <Card.Header>
              <Link to="/browse/models"><FontAwesomeIcon icon={faBackward}/></Link>
              <Card.Title>{this.state.model.name}</Card.Title>
              <Card.Subtitle>{this.state.model.desc}</Card.Subtitle>
            </Card.Header>
            <Card.Body>
              <Pentagon results={results}/>
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
