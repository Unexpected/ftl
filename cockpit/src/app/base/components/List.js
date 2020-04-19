import React from 'react';
import { connect } from 'react-redux';
import { LIST_LOAD } from '../../../constants/actionTypes';
import agent from '../../../agent.js';
import BootstrapTable from 'react-bootstrap-table-next';

const mapStateToProps = state => {
    return {
        listLoaded: state.common.viewLoaded,
        entities: state.common.module.entities,
        listData: state.common.viewData,
    }
};

const mapDispatchToProps = dispatch => ({
    onLoad: (payload) =>
        dispatch({ type: LIST_LOAD, payload }),
});

class List extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            loadedEntity: null,
            columns: []
        };
    }

    updateComponent() {
        const currentEntityName = this.props.match.params.entityName;
        if (this.state.loadedEntity === null || this.state.loadedEntity["name"] !== currentEntityName) {
            // display a new list

            // update columns in state and start fetching data
            const loadedEntity = this.props.entities[currentEntityName];
            const columns = []
            Object.entries(loadedEntity.attributes).forEach(([name, attribute]) => {
                columns.push({
                    dataField: name,
                    text: attribute.label
                });
            });
            agent.Entities.all(loadedEntity.name).then(this.setState({ "loadedEntity": loadedEntity, "columns": columns })).then(payload => this.props.onLoad(payload));
        }
    }

    componentDidMount() {
        this.updateComponent();
        //this.props.onLoad("entities");

        /*
         this.props.onLoad(Promise.all([
        agent.Articles.get(this.props.match.params.id),
        agent.Comments.forArticle(this.props.match.params.id)
        ]));
        */
    }

    componentDidUpdate() {
        this.updateComponent();
    }

    componentWillUnmount() {

    }

    render() {
        if (this.state.columns.length === 0) {
            return (<div>Loading list, please wait...</div>);
        }
        const rowEvents = {
            onClick: (e, row, rowIndex) => {
                this.props.history.push(`/entity/${row.entity_name}/${row.name}`)
            }
        };
        /*const rows = [];
        this.props.listData.forEach((row) => {
            rows.push(<div><div>{row.label}</div><div>{row.entity_name}</div><div>{row.name}</div></div>);
        });*/
        return (
            <div>
                Ceci est la liste des objets de type : {this.props.match.params.entityName}
                <BootstrapTable keyField='name' data={this.props.listData} columns={this.state.columns} rowEvents={rowEvents} />
            </div>
        );
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(List);
