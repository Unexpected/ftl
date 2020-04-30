import React from 'react';
import { connect } from 'react-redux';
import Home from './Home.js';
import List from './List.js';

const mapStateToProps = state => {
    return {
        currentView: state.common.currentView,
        listLoaded: state.common.viewLoaded,
        entities: state.common.module.entities,
    }
};

const mapDispatchToProps = dispatch => ({
    /*onLoad: (payload) =>
        dispatch({ type: LIST_LOAD, payload }), */
});


class View extends React.Component {

    render() {
        if (this.props.currentView === "default") {
            return <Home />
        }
        // return a list
        return <List entity={this.props.currentView} query={this.props.currentView} />

    }
}


export default connect(mapStateToProps, mapDispatchToProps)(View);
