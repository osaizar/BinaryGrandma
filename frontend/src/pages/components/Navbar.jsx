import React, { Component } from 'react'
import { Link } from 'react-router-dom';

import Image from 'react-bootstrap/Image';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

export default class NavbarComponent extends Component {
  constructor(props){
    super(props);
  }

  render(){
    return(
    <Navbar bg="light" expand="lg">
    <Navbar.Brand href="/">Binary Grandma</Navbar.Brand>
    <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link href="/">Analyze Binary</Nav.Link>
          <Nav.Link href="/upload_model">Upload Model</Nav.Link>
          <Nav.Link href="/browse">Browse</Nav.Link>
        </Nav>
      </Navbar.Collapse>
      <Navbar.Collapse className="justify-content-end">
        <Nav>
          <Nav.Link className="mr-auto" href="/jobs">Jobs</Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
    );
  }
}
