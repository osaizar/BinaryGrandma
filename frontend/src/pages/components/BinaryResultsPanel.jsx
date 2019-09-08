import React, { Component } from 'react'
import axios from 'axios';

import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Pentagon from './Pentagon';
import Loading from './Loading';

import {REMOTE_SERVER} from '../../config.js';

export default class BinaryResultsPanel extends Component {
  constructor(props){
    super(props);
    this.state = {
      results : [],
      limit : 3
    }
  }

  componentDidMount(){
    this.updateResults();
  }

  updateResults = () => {
    axios.get(REMOTE_SERVER+'/ajax/get_results/'+this.props.binary.id)
    .then(res => {
      if(res.status == 200){
        if (!res.data.analyzed){
          setTimeout(this.updateResults, 500);
        }

        this.setState({results : res.data.results, limit : res.data.results.length});
      }
    });
  }

  changeLimit = (event) => {
    event.preventDefault();
    this.setState({limit : event.target.value});
  }

  getSelectForm(){
    var options = this.state.results.map((e,i) => { return (<option key={i+1}>{i+1}</option>)});
    return(
      <Form.Control as="select" value={this.state.limit} onChange={this.changeLimit}>
        {options}
      </Form.Control>
    );
  }

  render(){
    if (this.state.results.length != 0){
      var showing = this.state.results;
      showing = showing.sort((a,b) =>  b.score - a.score);
      showing = showing.slice(0,this.state.limit);

      return(
        <Container>
          <Form>
            <Form.Group as={Form.Row} controlId="exampleForm.ControlSelect2">
              <Form.Label column sm={10}>Models to compare</Form.Label>
              <Col sm={2}>
                {
                  this.getSelectForm()
                }
              </Col>
            </Form.Group>
          </Form>
          <Pentagon results={showing}/>
        </Container>
      );
    }else{
      return(
        <Container>
          <Loading />
        </Container>
      );
    }
  }
}
