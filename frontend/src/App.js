import React from 'react'
import { Route, Switch } from 'react-router-dom';

import Container from 'react-bootstrap/Container';

import UploadBinaryPage from './pages/UploadBinaryPage';
import UploadModelPage from './pages/UploadModelPage';
import Browse from './pages/Browse';
import BinaryPage from './pages/BinaryPage';
import ModelPage from './pages/ModelPage';

import Navbar from './pages/components/Navbar';

export default function App() {
  return (
    <div>
      <Navbar/>
      <Container style={{"marginTop" : "3em"}}>
        <Switch>
          <Route exact path="/" component={UploadBinaryPage} />
          <Route exact path="/upload_model" component={UploadModelPage} />
          <Route exact path="/browse" component={Browse} />
          <Route path="/browse/:page" component={Browse} />
          <Route path="/bin/:id" component={BinaryPage} />
          <Route path="/model/:id" component={ModelPage} />
        </Switch>
      </Container>
    </div>
  )
}
