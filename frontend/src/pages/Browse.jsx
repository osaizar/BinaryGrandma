import React, { Component } from 'react';
import { Redirect } from 'react-router';

import Container from 'react-bootstrap/Container';
import Card from 'react-bootstrap/Card';
import Nav from 'react-bootstrap/Nav';

import BrowseBinaryTable from './components/BrowseBinaryTable';
import BrowseModelTable from './components/BrowseModelTable'

export default class Browse extends Component {
  constructor(props){
    super(props);
    this.state = {
      selected : "binaries"
    }
  }

  componentWillMount(){
    if (this.props.match.params.page){
      this.setState({selected : this.props.match.params.page});
    }
  }

  render(){
    var selected;

    if (this.state.selected == "models"){
      selected = (
        <BrowseModelTable/>
      );
    }else if(this.state.selected == "binaries"){
      selected = (
        <BrowseBinaryTable/>
      );
    }else{
      selected = (
        <Redirect to="/browse"/>
      )
    }

    return(
      <Container>
        <Card>
          <Card.Header>
            <Nav variant="tabs" activeKey={this.state.selected}>
              <Nav.Item>
                <Nav.Link eventKey="binaries" onClick={() => this.setState({selected : "binaries"})}>Binaries</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="models" onClick={() => this.setState({selected : "models"})}>Models</Nav.Link>
              </Nav.Item>
            </Nav>
          </Card.Header>
          <Card.Body>
            { selected }
          </Card.Body>
        </Card>
      </Container>
    );
  }
}
