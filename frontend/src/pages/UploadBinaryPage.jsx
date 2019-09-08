import React, { Component } from 'react';
import { Redirect } from 'react-router';
import axios from 'axios';

import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Container from 'react-bootstrap/Container';

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFileUpload } from "@fortawesome/free-solid-svg-icons";

import Loading from "./components/Loading"


export default class UploadBinaryPage extends Component {
  constructor(props){
    super(props);
    this.state = {
      selectedFile : null,
      name : "",
      state : "start",
      binary_id : null
    }
  }

  onChangeFile = (event) => {
    event.preventDefault();
    this.setState({
      selectedFile: event.target.files[0]
    })
  }

  onChangeName = (event) => {
    event.preventDefault();
    this.setState({
      name: event.target.value
    })
  }

  onClickButton = (event) => {
    event.preventDefault();

    axios.post('http://192.168.1.146:5000/ajax/create_binary', { "name" : this.state.name })
    .then(res => {
      if(res.status == 200){
        var binary = res.data.binary_id;
        this.setState({state : "uploading"})
        const data = new FormData();
        data.append('file', this.state.selectedFile);
        axios.post('http://192.168.1.146:5000/ajax/upload_binary_file/'+binary, data)
        .then(res => {
          if (res.status == 200){
            this.setState({state : "done", name : "",  selectedFile : null, binary_id : binary});
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
          <FontAwesomeIcon icon={faFileUpload} size="6x" style={{"margin-bottom" : "20px"}}/>
          <Form>
            <Form.Group controlId="formFileName">
              <Form.Label>File Name</Form.Label>
              <Form.Control type="text" value={this.state.name} onChange={this.onChangeName}/>
            </Form.Group>

            <Form.Group controlId="formModelFile">
              <Form.Label>Select a file</Form.Label>
              <Form.Control type="file" name="file" onChange={this.onChangeFile}/>
            </Form.Group>

            <Button onClick={this.onClickButton}>
              Upload File
            </Button>
          </Form>
        </Container>
      );
    }else if(this.state.state == "uploading"){
      return(
        <Loading text="Uploading file..."/>
      );
    }else{ // done
      return(
        <Redirect to={"/bin/"+this.state.binary_id}/>
      );
    }
  }
}
