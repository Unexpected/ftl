import React from 'react';
import Form from 'react-bootstrap/Form';
import agent from '../../../agent.js';
import { connect } from 'react-redux';
import { Button } from 'react-bootstrap';
import { ACTION_SAVE } from '../../../constants/actionTypes';

const mapStateToProps = state => {
    return {
        listLoaded: state.common.viewLoaded,
        entities: state.common.entities,
        listData: state.common.viewData,
    }
};

const mapDispatchToProps = dispatch => ({
    onSave: (payload) =>
        dispatch({ type: ACTION_SAVE, payload }),
});

class MyFormGroup extends React.Component {
    constructor(props) {
        super(props);
        this.textInput = React.createRef();
    }

    render() {
        return (
            /* <Form.Group controlId="formGroupEmail">
                    <Form.Label>Email address</Form.Label>
                    <Form.Control type="email" placeholder="Enter email" />
                    <Form.Control onChange={this.props.onChange} ref={this.textInput} placeholder={this.props.placeholder} />
                </Form.Group> */
            <div>
                <Form.Group controlId={this.props.id}>
                    <Form.Label>{this.props.label}</Form.Label>
                    <Form.Control onChange={this.props.onChange} value={this.props.value} placeholder={this.props.placeholder} />
                </Form.Group>
            </div>
        );
    }
}

class Action extends React.Component {
    constructor(props) {
        super(props);
        this.state = { form: {} };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        var formState = { ...this.state.form }
        formState[event.target.id] = event.target.value;
        this.setState({ form: formState });
    }


    handleSubmit(event) {
        console.log('Le formulaire a été soumis : ' + this.state.form.nom);
        agent.Person.create(this.state.form);
        event.preventDefault();
    }

    render() {

        const metadata = [];
        this.props.listData.forEach((row) =>
            metadata.push(
                <MyFormGroup id={row.name} label={row.label} onChange={this.handleChange} value={this.state.form[row.id]} placeholder={row.placeholder} />
            ));
        // const subForm = <MyFormGroup id="nom" label="Nom" onChange={this.handleChange} value={this.state.form.nom} placeholder="Entrez votre nom ici..." />

        return (
            <div>
                This is an action !
                <Form onSubmit={this.handleSubmit}>
                    <Button type="submit">Valider</Button>
                    {metadata}
                </Form>
            </div>
        );
    }

}

export default connect(mapStateToProps, mapDispatchToProps)(Action);