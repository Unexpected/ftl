import React from 'react';
import { connect } from 'react-redux';
import agent from '../../../agent.js';
import BootstrapTable from 'react-bootstrap-table-next';
import { VIEW_INITIALIZE } from '../../../constants/actionTypes.js';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { Button } from 'react-bootstrap';

const mapStateToProps = state => {
    return {
        entities: state.common.module.entities
    }
};

const mapDispatchToProps = dispatch => ({
    openAction: (entityName, keys) =>
        dispatch({ type: VIEW_INITIALIZE, viewName: "action", entityName: entityName, queryName: null, keys: keys })
});

class List extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            loadedEntity: null,
            columns: [],
            listData: null
        };
        this.handleAction = this.handleAction.bind(this);
    }

    handleAction(event) {
        const actionType = event.target.attributes.action.value;
        if (actionType === "create") {
            this.props.openAction(this.props.entityName, []);
        }
    }

    updateComponent() {
        if (this.state.loadedEntity === null || this.state.loadedEntity["name"] !== this.props.entityName) {
            // display a new list

            // update columns in state and start fetching data
            const loadedEntity = this.props.entities[this.props.entityName];
            const columns = []
            Object.entries(loadedEntity.attributes).forEach(([name, attribute]) => {
                columns.push({
                    dataField: name,
                    text: attribute.label
                });
            });

            agent.Query.fetch(this.props.queryName)
                .then(
                    payload => this.setState(
                        { "loadedEntity": loadedEntity, "columns": columns, listData: payload }));
        }
    }

    componentDidMount() {
        this.updateComponent();
    }

    componentDidUpdate() {
        this.updateComponent();
    }

    componentWillUnmount() {

    }

    render() {
        if (this.state.columns.length === 0 || this.state.loadedEntity == null) {
            return (<div>Loading list, please wait...</div>);
        }
        const rowEvents = {
            onClick: (e, row, rowIndex) => {
                this.props.openAction(this.props.entityName, [row._key_field_value]);
            }
        };
        return (
            <Container>
                <Row className="justify-content-md-center">Ceci est la liste des objets de type : {this.props.entityName}</Row>
                <Row><Button onClick={this.handleAction} action="create">Create new element</Button></Row>
                <Row>
                    <BootstrapTable keyField='_key_field_value' data={this.state.listData} columns={this.state.columns} rowEvents={rowEvents} />
                </Row>
            </Container>
        );
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(List);
