import React from 'react';
import View from '../components/View';
import { connect } from 'react-redux';

const mapDispatchToProps = dispatch => ({
    /* initialize: payload =>
        dispatch({ type: APP_INITIALIZE, payload }),
    selectModule: (moduleName, metadata) =>
        dispatch({ type: MODULE_INITIALIZE, moduleName: moduleName, metadata: metadata }) */
});

const mapStateToProps = state => {
    return {
        currentView: state.common.currentView
    }
};

class Content extends React.Component {

    render() {
        return (
            <View />
        )
    }
}

/* <Route path="/entity/:entityName" component={List} />
<Route path="/entity/:entityName/:id" component={Action} /> */

export default connect(mapStateToProps, mapDispatchToProps)(Content);