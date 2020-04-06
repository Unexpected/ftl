import React from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Header from './base/layout/Header.js';
import Content from './base/layout/Content.js';
import Footer from './base/layout/Footer.js';
import Container from 'react-bootstrap/Container';
import { connect } from 'react-redux';
import agent from '../agent.js';
import { APP_LOAD } from '../constants/actionTypes.js';

const mapDispatchToProps = dispatch => ({
  onLoad: payload =>
    dispatch({ type: APP_LOAD, payload })
});

const mapStateToProps = state => {
  return {
    appLoaded: state.common.appLoaded,
    entities: state.common.entities
  }
};

class App extends React.Component {
  componentDidMount() {
    Promise.all([
      agent.Entities.getAll()
    ]).then((data) => this.props.onLoad(data));
  }

  render() {
    if (!this.props.appLoaded) {
      return (<div>Loading... Please Wait...</div>);
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
