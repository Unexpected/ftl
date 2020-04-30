import React from 'react';
import Menu from './Menu.js';
import { connect } from 'react-redux';

const mapStateToProps = state => {
    return {
        module: state.common.module,
        entities: state.common.module.entities
    }
};

class Header extends React.Component {
    render() {
        return (
            <div id="header">
                <Menu module={this.props.module} entities={this.props.entities} />
            </div>
        );
    }
}

export default connect(mapStateToProps, null)(Header);
