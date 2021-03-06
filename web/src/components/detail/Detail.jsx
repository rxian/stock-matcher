import React from 'react';
import './Detail.scss';
import { withRouter } from "react-router";
import ListingDetail from "./ListingDetail";
import ListingPriceChart from "./ListingPriceChart";
import Similar from "./Similar";
import {defaultEndDate, defaultStartDate} from "../../static/hardCodeConfig";
import OptionsBar from "./OptionsBar";
import MentionedWith from "./MentionedWith";
import MentionedIn from "./MentionedIn";

class Detail extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            startDate: defaultStartDate,
            endDate: defaultEndDate,
        }
    }

    updateOptions = (startDate, endDate ) => {
        this.setState({ startDate: startDate, endDate: endDate});
    };

    render() {
        const id = this.props.match.params.id;
        const { startDate, endDate } = this.state;

        return (
            <div className="Detail">
                <ListingDetail listingID={id} date={endDate}/>
                <OptionsBar handleUpdateOptions={this.updateOptions}/>
                <ListingPriceChart listingID={id} startDate={startDate} endDate={endDate}/>
                <div className="row">
                    <Similar listingID={id} startDate={startDate} endDate={endDate}/>
                    <div className="space"/>
                    <div className="column">
                        <MentionedWith listingID={id}/>
                        <MentionedIn listingID={id}/>
                    </div>
                </div>
            </div>
        );
    }
}

export default withRouter(Detail);