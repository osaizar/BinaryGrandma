import React, { Component } from 'react';
import { Redirect } from 'react-router';

import Container from 'react-bootstrap/Container';
import Card from 'react-bootstrap/Card';
import Nav from 'react-bootstrap/Nav';

import JobsTable from './components/JobsTable';

export default class JobsPage extends Component {
  constructor(props){
    super(props);
    this.state = {
      selected : "running"
    }
  }

  componentWillMount(){
    if (this.props.match.params.page){
      this.setState({selected : this.props.match.params.page});
    }
  }

  render(){
    return(
      <Container>
        <Card>
          <Card.Header>
            <Nav variant="tabs" activeKey={this.state.selected}>
              <Nav.Item>
                <Nav.Link eventKey="running" onClick={() => this.setState({selected : "running"})}>Running</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="all" onClick={() => this.setState({selected : "all"})}>All</Nav.Link>
              </Nav.Item>
            </Nav>
          </Card.Header>
          <Card.Body>
            <JobsTable selected={this.state.selected}/>
          </Card.Body>
        </Card>
      </Container>
    );
  }
}
