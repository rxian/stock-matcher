import {useEffect, useState} from "react";
import API from "../../api";
import {Header, Label} from "semantic-ui-react";
import './ListingDetail.scss';

function ListingDetail({ listingID, date }) {
    const [detailData, setDetailData] = useState([]);
    const [priceData, setPriceData] = useState([]);

    const label = ["Technology", "Platform", "Hardware",
        "Cell Phone", "Tablet", "Digital Wellbeing", "Efficiency"];

    useEffect(() => {
        API.get(`/api/listings/${listingID}`, {
        }).then( res => {
            setDetailData(res.data.data);
        }).catch(e => {});

        API.get(`/api/listings/${listingID}/prices`, {
            params: {
                "start-date": date,
                "end-date": date,
            }
        }).then(res => {
            if (res.data && res.data.data.length !== 0) {
                setPriceData(res.data.data[0]);
            }
        }).catch(e => {})
    }, [listingID, date]);

    return (
        <div className="ListingDetail">
            {detailData &&
            <div className="left">
                <Header as="h1"> {detailData.symbol}</Header>
                <span className="description"> {detailData.name} </span>
            </div>
            }
            <div className="right">
                <Header as="h1"> {priceData.length !== 0? priceData.close.toFixed(2): null}</Header>
                <div className="tags">
                    {label.map(l => <Label size="tiny" color="teal" key={l}> {l} </Label>)}
                </div>
            </div>
        </div>
    );
}

export default ListingDetail;