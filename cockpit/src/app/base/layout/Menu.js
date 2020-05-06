import React from 'react';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { VIEW_INITIALIZE } from '../../../constants/actionTypes.js';
import { connect } from 'react-redux';


const mapDispatchToProps = dispatch => ({
    selectView: (viewName, entityName) =>
        dispatch({ type: VIEW_INITIALIZE, viewName: viewName, entityName: entityName, queryName: entityName, keys: [] })
});

class Menu extends React.Component {

    constructor(props) {
        super(props);
        this.state = {};
        this.handleMenuSelect = this.handleMenuSelect.bind(this);
    }

    componentDidMount() {
    }

    componentDidUpdate() {

    }

    handleMenuSelect(event) {
        const entityName = event.target.attributes.entityName.value;
        const viewName = event.target.attributes.viewName.value;
        this.props.selectView(viewName, entityName);
    }

    render() {

        const navItems = [];
        Object.entries(this.props.entities).forEach(([name, entity]) => {
            // const entity = e[0];
            navItems.push(<Nav.Link key={name} entityname={name} viewname="list" onClick={this.handleMenuSelect}> {entity.label}</Nav.Link>)
        });

        return (
            <Navbar bg="dark" variant="dark" sticky="top" expand="lg" >
                <Navbar.Brand viewname="default" entityname="" onClick={this.handleMenuSelect}>{this.props.module.label}</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="mr-auto">
                        {navItems}
                    </Nav>
                    {/* TODO : Quicksearch ? 
                    <Form inline>
                        <FormControl type="text" placeholder="Search" className="mr-sm-2" />
                        <Button variant="outline-success">TODO</Button>
                    </Form>*/}
                </Navbar.Collapse>
            </Navbar>
        );
    }
}

export default connect(null, mapDispatchToProps)(Menu);
