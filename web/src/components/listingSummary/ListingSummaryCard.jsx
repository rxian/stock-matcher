import {useEffect, useState} from "react";
import API from "../../api";
import LineChart from "../chart/Chart";

function ListingSummaryCard({ listingID,
                                title,
                                description,
                                price,
                                startDate,
                                endDate,
                                width,
                                height,
                                content,
                                strokeColor,
                                strokeWidth
                            }) {
    const [data, setData] = useState([]);

    useEffect(() => {
        let isMounted = true; // NOTE: isMounted variable is used to avoid warnings when using React hook with async function.
        API.get(`/api/listings/${listingID}/prices`, {
            params: {
                "start-date": startDate,
                "end-date": endDate,
            }
        }).then((res) => {
            if (!isMounted) return;
            setData(res.data.data);
        }).catch((e) => {});
        return () => { isMounted = false };
    }, [listingID, startDate, endDate]);

    return (
        <div className="ListingSummaryCard">
            <div key='image' className='image'>
                {data.length === 0? null:
                    <LineChart
                        data={data.map(item => ({
                            x: new Date(item.date),
                            y: item.close,
                        }))}
                        height={height? height: 42}
                        width={width? width: 70}
                        normal
                        strokeColor={strokeColor}
                        strokeWidth={strokeWidth}
                    />
                }
            </div>
            <div key='content' className='content'>
                {
                    content? content: <div>
                        { title && <div className='title'>{title}</div> }
                        { description && <div className='description'>{description}</div> }
                    </div>
                }
                { price && data.length !== 0 && <div className='price'>{data[data.length-1].close.toFixed(2)}</div> }
            </div>
        </div>
    );
}

export default ListingSummaryCard;