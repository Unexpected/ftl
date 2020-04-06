import React from 'react';
import Home from '../components/Home';
import List from '../components/List';
import Action from '../components/Action';
import { Route, Switch } from 'react-router-dom';


function Content(props) {
    return (
        <Switch>
            <Route exact path="/" component={Home} />
            <Route path="/entities" component={List} />
            <Route path="/queries" component={List} />
            <Route path="/entity/:entityName/:id" component={Action} />
            <Route path="/entity/:entityName" component={List} />
        </Switch>
    );
}

export default Content;