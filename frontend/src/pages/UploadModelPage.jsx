import React, { Component } from 'react';
import { Redirect } from 'react-router'
import axios from 'axios';

import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Container from 'react-bootstrap/Container';

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFileArchive } from "@fortawesome/free-solid-svg-icons";

import Loading from "./components/Loading";

import {REMOTE_SERVER} from '../config.js';

export default class UploadModelPage extends Component {
  constructor(props){
    super(props);
    this.state = {
      selectedFile : null,
      name : "",
      desc : "",
      benign : false,
      state : "start",
      model_id : null
    }
  }

  onChangeName = (event) => {
    event.preventDefault();
    this.setState({
      name: event.target.value
    })
  }

  onChangeDesc = (event) => {
    event.preventDefault();
    this.setState({
      desc : event.target.value
    })
  }

  onChangeBenign = (event) => {
    event.preventDefault();
    if (event.target.id){
      this.setState({benign : false});
    }else{
      this.setState({benign : true});
    }
  }

  onChangeFile = (event) => {
    event.preventDefault();
    this.setState({
      selectedFile: event.target.files[0]
    })
  }

  onClickButton = (event) => {
    event.preventDefault();
    axios.post(REMOTE_SERVER+'/ajax/create_model', { "name" : this.state.name, "desc" : this.state.desc, "benign" : this.state.benign})
    .then(res => {
      if(res.status == 200){
        var model = res.data.model_id;
        this.setState({state : "uploading"})
        const data = new FormData();
        data.append('file', this.state.selectedFile);
        axios.post(REMOTE_SERVER+'/ajax/upload_model_file/'+model, data)
        .then(res => {
          if (res.status == 200){
            this.setState({state : "done", name : "", desc : "", benign : false, selectedFile : null, model_id : model});
          }
        });
      }
    });
  }

  onClickStartNew = (event) => {
    event.preventDefault();
    this.setState({state : "start"});
  }

  render(){
    if (this.state.state == "start"){
      return(
        <Container>
          <FontAwesomeIcon icon={faFileArchive} size="6x" style={{"margin-bottom" : "20px"}}/>
          <Form>
            <Form.Group controlId="formModelName">
              <Form.Label>Model Name</Form.Label>
              <Form.Control type="text" value={this.state.name} onChange={this.onChangeName}/>
            </Form.Group>

            <Form.Group controlId="formModelDesc">
              <Form.Label>Description</Form.Label>
              <Form.Control as="textarea" rows="3" value={this.state.desc} onChange={this.onChangeDesc}/>
            </Form.Group>

            <Form.Group controlId="formModelBenign">
              <Form.Label>Is this malware?</Form.Label>
              <Form.Control as="select" onChange={this.onChangeBenign}>
                <option id="malware">Yes, it's malware</option>
                <option id="benign">No, it's benign software</option>
              </Form.Control>
            </Form.Group>

            <Form.Group controlId="formModelFile">
              <Form.Label>ZIP File</Form.Label>
              <Form.Control type="file" name="file" onChange={this.onChangeFile}/>
            </Form.Group>

            <Button onClick={this.onClickButton}>
              Upload Model
            </Button>
          </Form>
        </Container>
      );
    }else if(this.state.state == "uploading"){
      return(
        <Loading text="uploading file..."/>
      );
    }else{ // done
      return(
        <Redirect to={"/model/"+this.state.model_id}/>
      );
    }
  }
}
