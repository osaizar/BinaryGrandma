import React, { Component } from 'react'
import axios from 'axios';

import Table from 'react-bootstrap/Table';


export default class BinaryResultsTable extends Component {
  constructor(props){
    super(props);
    this.state = {
      results : []
    }
  }

  componentWillMount(){
    axios.get('http://localhost:5000/ajax/get_results/'+this.props.binary.id)
    .then(res => {
      if(res.status == 200){
        this.setState({results : res.data.results})
      }
    });
  }

  listResults = (e, i) => {
    return(
      <tr key={i}>
        <th>{i}</th>
        <th>{e.model}</th>
        <th>{e.score}</th>
      </tr>
    );
  }

  render(){
    return(
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>#</th>
            <th>Model Name</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {
            this.state.results.map(this.listResults)
          }
        </tbody>
      </Table>
    );
  }
}
