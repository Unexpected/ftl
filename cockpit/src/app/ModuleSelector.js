import React from 'react';
import Card from 'react-bootstrap/Card';
import CardDeck from 'react-bootstrap/CardDeck';
import Button from 'react-bootstrap/Button';

class ModuleSelector extends React.Component {

    componentDidMount() {

    }

    componentDidUpdate() {

    }

    render() {
        const moduleItems = [];

        // <Card.Link href="#">Card Link</Card.Link> ???? 
        this.props.modules.forEach((module) => {
            // const entity = e[0];
            moduleItems.push(
                <Card key={'card-' + module.name} bg='dark' text="white" className="mx-auto" style={{ width: '18rem', flex: 'inherit' }}>
                    <Card.Img variant="top" src="logo192.png" />
                    <Card.Body>
                        <Card.Title>{module.label}</Card.Title>
                        <Card.Text>
                            {module.comment}
                        </Card.Text>
                        <Button onClick={this.props.onModuleSelect} value={module.name}>Go</Button>
                    </Card.Body>
                </Card>
            );
        });
        return (
            <CardDeck>
                {moduleItems}
            </CardDeck>
        );
    }
}

export default ModuleSelector;