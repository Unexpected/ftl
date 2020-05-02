import React from 'react';
import { connect } from 'react-redux';
import Home from './Home.js';
import List from './List.js';
import Action from './Action.js';

const mapStateToProps = state => {
    return {
        view: state.common.view,
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
        if (this.props.view.name === "default") {
            return <Home />
        }

        if (this.props.view.name === "action") {
            return <Action entityName={this.props.view.entityName} keys={this.props.view.keys} />
        }

        if (this.props.view.name === "list") {
            // return a list
            return <List entityName={this.props.view.entityName} queryName={this.props.view.queryName} />
        }

        return <div>view "{this.props.view.name}" does not exists</div>
    }

}


export default connect(mapStateToProps, mapDispatchToProps)(View);
