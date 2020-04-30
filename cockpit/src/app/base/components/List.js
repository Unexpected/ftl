import React from 'react';
import { connect } from 'react-redux';
import agent from '../../../agent.js';
import BootstrapTable from 'react-bootstrap-table-next';

const mapStateToProps = state => {
    return {
        entities: state.common.module.entities
    }
};

const mapDispatchToProps = dispatch => ({

});

class List extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            loadedEntity: null,
            columns: [],
            listData: null
        };
    }

    updateComponent() {
        if (this.state.loadedEntity === null || this.state.loadedEntity["name"] !== this.props.entity) {
            // display a new list

            // update columns in state and start fetching data
            const loadedEntity = this.props.entities[this.props.entity];
            const columns = []
            Object.entries(loadedEntity.attributes).forEach(([name, attribute]) => {
                columns.push({
                    dataField: name,
                    text: attribute.label
                });
            });

            agent.Query.fetch(this.props.query)
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
            /* onClick: (e, row, rowIndex) => {
                this.props.history.push(`/entity/${row.entity_name}/${row.name}`)
            } */
        };
        /*const rows = [];
        this.props.listData.forEach((row) => {
            rows.push(<div><div>{row.label}</div><div>{row.entity_name}</div><div>{row.name}</div></div>);
        });*/

        return (
            <div>
                Ceci est la liste des objets de type : {this.props.entityName}
                <BootstrapTable keyField='_key_field_value' data={this.state.listData} columns={this.state.columns} rowEvents={rowEvents} />
            </div>
        );
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(List);
