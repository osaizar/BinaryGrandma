import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

import Table from 'react-bootstrap/Table';


export default class BrowseModelTable extends Component {
  constructor(props){
    super(props);
    this.state = {
      models : []
    }
  }

  componentWillMount(){
    axios.get('http://localhost:5000/ajax/get_models')
    .then(res => {
      if(res.status == 200){
        this.setState({models : res.data.models})
      }
    });
  }

  listModels = (e, i) => {
    var link = "/model/"+e.id
    return(
      <tr key={i}>
        <th>{e.id}</th>
        <th><Link to={link}>{e.name}</Link></th>
        <th>{e.desc}</th>
        <th>{e.analyzed.toString()}</th>
      </tr>
    );
  }

  render(){
    return(
      <Table striped bordered hover responsive >
        <thead>
          <tr>
            <th>#</th>
            <th>Model name</th>
            <th>Description</th>
            <th>Available</th>
          </tr>
        </thead>
        <tbody>
          {
            this.state.models.map(this.listModels)
          }
        </tbody>
      </Table>
    );
  }
}
