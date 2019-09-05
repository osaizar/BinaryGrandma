import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

import Table from 'react-bootstrap/Table';


export default class BrowseBinaryTable extends Component {
  constructor(props){
    super(props);
    this.state = {
      binaries : []
    }
  }

  componentWillMount(){
    axios.get('http://localhost:5000/ajax/get_binaries')
    .then(res => {
      if(res.status == 200){
        this.setState({binaries : res.data.binaries})
      }
    });
  }

  listBinaries = (e, i) => {
    var link = "/bin/"+e.id
    return(
      <tr key={i}>
        <th>{e.id}</th>
        <th><Link to={link}>{e.name}</Link></th>
        <th>{e.hash}</th>
        <th>{e.date}</th>
      </tr>
    );
  }

  render(){
    return(
      <Table striped bordered hover responsive >
        <thead>
          <tr>
            <th>#</th>
            <th>Binary name</th>
            <th>Hash</th>
            <th>Input date</th>
          </tr>
        </thead>
        <tbody>
          {
            this.state.binaries.map(this.listBinaries)
          }
        </tbody>
      </Table>
    );
  }
}
