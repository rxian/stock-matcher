import React from "react";
import {Button, Form, Icon, Message, Modal} from "semantic-ui-react";
import API from "../api";
import './Modal.scss';

class AddModal extends React.Component {
    state = {
        company: "",
        symbol: "",
        active: false,
        tracked: false,
        success: false,
    };

    handleChange = (e, { name, value }) => {
        this.setState({ [name]: value });
    };

    handleSubmit = () => {
        const { company, symbol, active, tracked } = this.state;
        const { updateHandler } = this.props;

        console.log(`submit new entry: ${company}, ${symbol}`);
        API.post('/api/listings/', {
            name: company,
            symbol: symbol,
            active: active,
            tracked: tracked,
        }).then((res) => {
            this.setState({
                success: true,
            });
            updateHandler();
        }).catch((error) => {
            alert(error);
        });
    };

    render() {
        const { success } = this.state;
        return (
            <Modal trigger={<Button icon><Icon name='add'/></Button>}>
                <Modal.Header>Add</Modal.Header>
                <Form onSubmit={this.handleSubmit} success={success}>
                    <Message
                        success
                        header="Success"
                    />
                    <Form.Input
                        label="Company"
                        name="company"
                        onChange={this.handleChange}
                    />
                    <Form.Input
                        label="Symbol"
                        name="symbol"
                        onChange={this.handleChange}
                    />
                    <Button type='submit' primary>Submit</Button>
                </Form>
            </Modal>
        );
    }
}

class EditModal extends React.Component {
    state = {
        name: "",
        symbol: "",
        active: false,
        tracked: false,
        success: false,
    };

    componentDidMount() {
        const { symbolOld, nameOld } = this.props;
        this.setState({
            name: nameOld !== undefined? nameOld: "",
            symbol: symbolOld !== undefined? symbolOld: "",
        })
    }

    handleChange = (e, { name, value }) => {
        console.log(name, value);
        this.setState({ [name]: value });
    };

    handleSubmit = () => {
        const { listingID, updateHandler } = this.props;
        const { name, symbol, active, tracked } = this.state;

        API.put(`/api/listings/${listingID}`, {
            name: name,
            symbol: symbol,
            active: active,
            tracked: tracked,
        }).then((res) => {
            this.setState({
                success: true,
            });
            updateHandler();
        }).catch((e) => {
            console.log(e);
            alert(e);
        });
    };

    handleDeleteOnClick = () => {
        const { listingID, updateHandler } = this.props;
        API.delete(`/api/listings/${listingID}`)
            .then((res) => {
                console.log(res);
                alert("deleted");
                updateHandler();
            }).catch((e) => {
            console.log(e)
        })
    };

    render() {
        const { listingID } = this.props;
        const { success, name, symbol } = this.state;
        return (
            <Modal trigger={<Button icon><Icon name='edit'/></Button>}>
                <Modal.Header>{`Edit Listing: ${listingID}`}</Modal.Header>
                <Form onSubmit={this.handleSubmit} success={success}>
                    <Message
                        success
                        header="Success"
                    />
                    <Form.Input
                        label="Company"
                        name="name"
                        value={name}
                        onChange={this.handleChange}
                    />
                    <Form.Input
                        label="Symbol"
                        name="symbol"
                        value={symbol}
                        onChange={this.handleChange}
                    />
                    <Button type='submit' primary>Submit</Button>
                    <Button
                        type="button"
                        negative
                        onClick={this.handleDeleteOnClick}
                        className="delete-button"
                    >
                        <Icon name='trash alternate' />
                        Delete Entry
                    </Button>
                </Form>
            </Modal>
        );
    }
}

export { AddModal, EditModal };

// class ModalForm extends React.Component {
//     state = {
//         success: false,
//     };
//
//     handleSubmit = () => {
//         const { handleSubmit } = this.props;
//         handleSubmit()
//             .then(() => {
//                 this.setState({
//                     success: true,
//                 })
//             }).catch((e) => {
//
//         })
//     };
//
//     render() {
//         const { trigger, header } = this.props;
//         const { success } = this.state;
//         return (
//             <Modal trigger={trigger}>
//                 <Modal.Header>{header}</Modal.Header>
//                 <Form onSubmit={this.handleSubmit} success={success}>
//                     <Message
//                         success
//                         header="Success"
//                     />
//                     { this.props.children }
//                 </Form>
//             </Modal>
//         );
//     }
// }