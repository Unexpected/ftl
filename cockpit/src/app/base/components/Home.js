import React from 'react';
import { MODULE_UNLOAD } from '../../../constants/actionTypes.js';
import { connect } from 'react-redux';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { Button } from 'react-bootstrap';

const mapDispatchToProps = dispatch => ({
    deselectModule: (moduleName, metadata) =>
        dispatch({ type: MODULE_UNLOAD })
});

const mapStateToProps = state => {
    return {
        modules: state.common.modules,
        module: state.common.module,
    }
};

class Home extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
        this.handleModuleUnload = this.handleModuleUnload.bind(this);
    }

    handleModuleUnload(event) {
        this.props.deselectModule();
    }

    render() {
        return (
            <div>
                <Container>
                    <Row className="justify-content-md-center">This is home</Row>
                    <Row>Loaded module: {this.props.module.name} - {this.props.module.label}</Row>
                    <Row>Loaded module: {this.props.module.comment}</Row>
                    <Row>Module has {Object.entries(this.props.module.entities).length} entities</Row>
                    <Row><Button onClick={this.handleModuleUnload}>Select another module</Button></Row>
                </Container>
            </div>
        );
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Home);
