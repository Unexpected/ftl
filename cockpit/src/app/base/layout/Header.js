import React from 'react';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { connect } from 'react-redux';

import { Link } from 'react-router-dom';

const mapStateToProps = state => {
    return {
        module: state.common.module,
        entities: state.common.module.entities
    }
};

class Menu extends React.Component {

    componentDidMount() {

    }

    componentDidUpdate() {

    }

    render() {

        const navItems = [];
        Object.entries(this.props.entities).forEach(([name, entity]) => {
            // const entity = e[0];
            navItems.push(<Nav.Link as={Link} key={name} to={"/entity/" + name}>{entity.label}</Nav.Link>)
        });

        return (
            <Navbar bg="dark" variant="dark" sticky="top" expand="lg">
                <Navbar.Brand as={Link} to="/">{this.props.module.label}</Navbar.Brand>
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

class Header extends React.Component {
    render() {
        return (
            <div id="header">
                <Menu module={this.props.module} entities={this.props.entities} />
            </div>
        );
    }
}

export default connect(mapStateToProps)(Header);
