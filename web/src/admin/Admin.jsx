import React from 'react';
import './Admin.css';
import {Button, Modal, Form, Search} from 'semantic-ui-react';

function Admin() {
    return (
        <div className="Admin">
            <AddModal/>
            <EditSearch/>
        </div>
    );
}

export default Admin;

class AddModal extends React.Component {
    render() {
        return (
            <Modal
                trigger={<Button>Add Entry</Button>}
            >
                <Modal.Header>Add Entry</Modal.Header>
                <Form>
                    <Form.Input label="Company" required/>
                    <Form.Input label="Symbol" required/>
                    <Button type='submit'>Submit</Button>
                </Form>
            </Modal>
        )
    }
}

class EditSearch extends React.Component {
    render() {
        return (
            <Search/>
        )
    }
}