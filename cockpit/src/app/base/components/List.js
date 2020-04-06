import React from 'react';
import { connect } from 'react-redux';
import { LIST_LOAD } from '../../../constants/actionTypes';
import agent from '../../../agent.js';
import BootstrapTable from 'react-bootstrap-table-next';

const mapStateToProps = state => {
    return {
        listLoaded: state.common.viewLoaded,
        entities: state.common.entities,
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
            loadedEntity: null
        };
    }

    fetchData() {
        const currentEntity = this.props.match.params.entityName;
        if (this.state.loadedEntity !== currentEntity) {
            agent.Attributes.all(currentEntity).then(this.setState({ loadedEntity: currentEntity })).then(payload => this.props.onLoad(payload));
        }
    }

    componentDidMount() {
        console.log("this should start a dispatch");
        this.fetchData();
        //this.props.onLoad("entities");

        /*
         this.props.onLoad(Promise.all([
        agent.Articles.get(this.props.match.params.id),
        agent.Comments.forArticle(this.props.match.params.id)
        ]));
        */
    }

    componentDidUpdate() {
        this.fetchData();

        console.log("update, entity name is now : " + this.props.match.params.entityName);
    }

    componentWillUnmount() {

    }

    render() {
        if (this.props.listLoaded) {
            const columns = [{
                dataField: 'entity_name',
                text: 'entity_name'
            }, {
                dataField: 'name',
                text: 'name'
            }, {
                dataField: 'label',
                text: 'label'
            }, {
                dataField: 'length',
                text: 'length'
            }, {
                dataField: 'mandatory',
                text: 'mandatory'
            }];

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
                    <BootstrapTable keyField='name' data={this.props.listData} columns={columns} rowEvents={rowEvents} />
                </div>
            );
        }
        return (
            <div>
                Loading... Please wait...
            </div>
        );
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(List);
