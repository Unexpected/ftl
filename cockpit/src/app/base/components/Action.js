import React from 'react';
import Form from 'react-bootstrap/Form';
import agent from '../../../agent.js';
import { connect } from 'react-redux';
import { Button } from 'react-bootstrap';
import { ACTION_SAVE } from '../../../constants/actionTypes';

const mapStateToProps = state => {
    return {
        models: state.common.module.entities
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
        if (this.props.readonly) {
            return (
                <Form.Group controlId={this.props.id}>
                    <Form.Label>{this.props.label}</Form.Label>
                    <Form.Control value={this.props.value} plaintext readonly />
                </Form.Group>
            )
        }

        return (
            <Form.Group controlId={this.props.id}>
                <Form.Label>{this.props.label}</Form.Label>
                <Form.Control onChange={this.props.onChange} value={this.props.value} placeholder={this.props.placeholder} />
            </Form.Group>
        );
    }
}

class Action extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            form: {},
            entityModel: null,
            formModel: null
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        var formState = { ...this.state.form }
        formState[event.target.id] = event.target.value;
        this.setState({ form: formState });
    }


    handleSubmit(event) {
        agent.Entity.update(this.props.entityName, this.state.form);
        console.log('Le formulaire a été soumis : ' + this.state.form);
        //agent.Person.create(this.state.form);
        event.preventDefault();
    }

    updateComponent() {
        if (this.state.entityModel === null || this.state.entityModel["name"] !== this.props.entityName) {
            // update metadata
            const entityModel = this.props.models[this.props.entityName];

            if (this.props.keys !== null && this.props.keys.length === 1) {
                // fetch one entity
                agent.Entity.fetchOne(this.props.entityName, this.props.keys[0])
                    .then(entity => {
                        var formState = { ...this.state.form }
                        Object.entries(entityModel.attributes).forEach(([name, attribute]) => {
                            if (entity[name] === null) {
                                formState[name] = "";
                            } else {
                                formState[name] = entity[name];
                            }
                        });

                        this.setState({ "entityModel": entityModel, "form": formState });
                    });
            } else {
                this.setState({ "entityModel": entityModel });
            }
        }
    }

    componentDidMount() {
        this.updateComponent();
    }

    componentDidUpdate() {
        this.updateComponent();
    }

    render() {
        if (this.state.entityModel === null) {
            return <div>Loading...</div>
        }
        const formModel = [];
        Object.entries(this.state.entityModel.attributes).forEach(([name, attribute]) => {
            const readonly = this.state.entityModel.primary_key.includes(name);
            formModel.push(
                <MyFormGroup id={name} key={name} label={attribute.label} onChange={this.handleChange} value={this.state.form[name]} placeholder={attribute.placeholder} readonly={readonly} />
            )
        });
        /* const metadata = [];
        this.props.listData.forEach((row) =>
            metadata.push(
                <MyFormGroup id={row.name} label={row.label} onChange={this.handleChange} value={this.state.form[row.id]} placeholder={row.placeholder} />
            ));
            */
        // const subForm = <MyFormGroup id="nom" label="Nom" onChange={this.handleChange} value={this.state.form.nom} placeholder="Entrez votre nom ici..." />

        return (
            <div>
                This is an action !
                <Form onSubmit={this.handleSubmit}>
                    <Button type="submit">Valider</Button>
                    {formModel}
                </Form>
            </div>
        );
    }

}

export default connect(mapStateToProps, mapDispatchToProps)(Action);