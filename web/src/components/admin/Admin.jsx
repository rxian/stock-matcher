import React from 'react';
import './Admin.scss';
import {Table} from 'semantic-ui-react';
import API from '../../api';
import {AddModal, EditModal} from "./Modal";

class Admin extends React.Component{
    constructor(props) {
        super(props);

        this.state = {
            data: []
        };
    }

    getData = () => {
        console.log("getting data");
        API.get('/api/listings')
            .then(res => {
                this.setState({
                    data: res.data['data'],
                })
            })
    };

    componentDidMount() {
        this.getData()
    }

    render(){
        const { data } = this.state;

        return (
            <div className="Admin">
                {/*<EditSearch/>*/}
                <AdminTable data={data} updateHandler={this.getData}/>
            </div>
        );
    }
}

export default Admin;

class AdminTable extends React.Component {
    render() {
        const { data, updateHandler } = this.props;

        if (data === null) {
            console.log('no data yet');
        }

        data.sort((a, b) => {
           return a['listingID']-b['listingID'];
        });

        const rows = data.map((item) => {
            return (
                <Table.Row key={item['listingID']}>
                    <Table.Cell>
                        {item['listingID']}
                    </Table.Cell>
                    <Table.Cell>
                        {item['symbol']}
                    </Table.Cell>
                    <Table.Cell>
                        {item['name']}
                    </Table.Cell>
                    {/*<Table.Cell>*/}
                    {/*    {item['active']? <Icon name="checkmark"/>:*/}
                    {/*            <Icon name="close"/>}*/}
                    {/*</Table.Cell>*/}
                    {/*<Table.Cell>*/}
                    {/*    {item['tracked']? <Icon name="checkmark"/>:*/}
                    {/*        <Icon name="close"/>}*/}
                    {/*</Table.Cell>*/}
                    <Table.Cell>
                        <EditModal
                            nameOld={item['name']}
                            symbolOld={item['symbol']}
                            listingID={item['listingID']}
                            active={item['active'] !== 0}
                            tracked={item['tracked'] !== 0}
                            updateHandler={updateHandler}
                        />
                    </Table.Cell>
                </Table.Row>
            )
        });
        return (
            <div>

                <Table celled>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell>Listing ID</Table.HeaderCell>
                            <Table.HeaderCell>Symbol</Table.HeaderCell>
                            <Table.HeaderCell>Name</Table.HeaderCell>
                            {/*<Table.HeaderCell>Active</Table.HeaderCell>*/}
                            {/*<Table.HeaderCell>Tracked</Table.HeaderCell>*/}
                            <Table.HeaderCell><AddModal updateHandler={updateHandler}/></Table.HeaderCell>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {rows}
                    </Table.Body>
                </Table>
            </div>

        )
    }
}

