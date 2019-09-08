import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

import Table from 'react-bootstrap/Table';


export default class JobsTable extends Component {
  constructor(props){
    super(props);
    this.state = {
      jobs : [],
      selected : "running"
    }
  }

  componentDidMount(){
    this.updateJobs()
  }

  componentDidUpdate(){
    if (this.props.selected != this.state.selected){
      this.setState({selected : this.props.selected})
      this.updateJobs();
    }
  }

  updateJobs = () => {
    if (this.props.selected == "running"){
      this.getRunningJobs();
    }else{
      this.getAllJobs();
    }
  }

  getAllJobs = () => {
    axios.get('http://192.168.1.146:5000/ajax/get_jobs')
    .then(res => {
      if(res.status == 200){
        this.setState({jobs : res.data.jobs});
      }
    });
  }

  getRunningJobs = () => {
    axios.get('http://192.168.1.146:5000/ajax/get_running_jobs')
    .then(res => {
      if(res.status == 200){
        if (res.data.jobs.length != 0){
          setTimeout(this.updateResults, 500);
        }
        this.setState({jobs : res.data.jobs})
      }
    });
  }

  getTableHead = () => {
    if (this.state.selected == "running"){
      return(
        <thead>
          <tr>
            <th>#</th>
            <th>Job name</th>
            <th>Start Time</th>
            <th>Log</th>
          </tr>
        </thead>
      );
    }else{
      return(
        <thead>
          <tr>
            <th>#</th>
            <th>Job name</th>
            <th>Start Time</th>
            <th>Ended</th>
            <th>End Time</th>
            <th>Log</th>
          </tr>
        </thead>
      );
    }
  }

  getLogTable = (log) => {
    log = log.split("\n");
    log.pop();
    return(
      <Table triped bordered size={"sm"} responsive className="table-sm">
        <tbody>
          {
            log.map(l => (
              <tr>
                <th>{l}</th>
              </tr>
            ))
          }
        </tbody>
      </Table>
    );
  }

  listRunning = (e,i) => {
    return(
      <tr key={i}>
        <th>{e.id}</th>
        <th>{e.name}</th>
        <th>{e.start_time}</th>
        <th>{this.getLogTable(e.log)}</th>
      </tr>
    );
  }

  listAll = (e,i) => {
    return(
      <tr key={i}>
        <th>{e.id}</th>
        <th>{e.name}</th>
        <th>{e.start_time}</th>
        <th>{e.ended}</th>
        <th>{e.end_time}</th>
        <th>{this.getLogTable(e.log)}</th>
      </tr>
    );
  }

  getTableBody= () => {
    if (this.props.selected == "running"){
      return(
        <tbody>
          {
            this.state.jobs.map(this.listRunning)
          }
        </tbody>
      );
    }else{
      return(
        <tbody>
          {
            this.state.jobs.map(this.listAll)
          }
        </tbody>
      );
    }
  }

  render(){
    return(
      <Table striped bordered hover responsive >
        { this.getTableHead() }
        { this.getTableBody() }
      </Table>
    );
  }
}
