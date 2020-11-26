import {useEffect, useState} from "react";
import API from "../../api";
import LineChart from "../chart/Chart";
import {Loader} from "semantic-ui-react";

function ListingPriceChart({ listingID, startDate, endDate }) {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        setLoading(true);
        API.get(`/api/listings/${listingID}/prices`, {
            params: {
                "start-date": startDate,
                "end-date": endDate,
            }
        }).then((res) => {
            setData(res.data.data);
            setLoading(false);
        }).catch((e) => {
            setData([]);
            setLoading(false);
        });
    }, [listingID, startDate, endDate]);

    const content = data.length === 0? <p>No data</p>:
        (<LineChart
            data={data.map(item => ({
                x: new Date(item.date),
                y: item.close,
            }))}
            height={400}
            width={822}
            axis
        />);
    return (
        <div className="ListingPriceChart">
            {
                loading? <Loader active/>:
                    content
            }
        </div>
    );
}

export default ListingPriceChart;