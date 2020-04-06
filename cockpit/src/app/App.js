import React from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Header from './base/layout/Header.js';
import Content from './base/layout/Content.js';
import Footer from './base/layout/Footer.js';
import Container from 'react-bootstrap/Container';
import ModuleSelector from './ModuleSelector.js';
import { connect } from 'react-redux';
import agent from '../agent.js';
import { APP_INITIALIZE } from '../constants/actionTypes.js';

const mapDispatchToProps = dispatch => ({
  initialize: payload =>
    dispatch({ type: APP_INITIALIZE, payload })
});

const mapStateToProps = state => {
  return {
    appInitialized: state.common.appInitialized,
    modules: state.common.modules,
    appLoaded: state.common.appLoaded,
    entities: state.common.entities
  }
};

class App extends React.Component {
  componentDidMount() {
    // Initialize application by getting all available modules
    Promise.all([
      agent.App.modules()
    ]).then((data) => this.props.initialize(data));
  }

  render() {
    if (!this.props.appInitialized) {
      return (<div>Loading... Please Wait...</div>);
    }
    if (!this.props.currentModule) {
      return (<div className="App">
        <ModuleSelector modules={this.props.modules} />
      </div>);
    }
    return (
      <div className="App">
        <Container>
          <Header entities={this.props.entities} />
          <Content />
          <Footer />
        </Container>
      </div>
    );
  }

}
export default connect(mapStateToProps, mapDispatchToProps)(App);
