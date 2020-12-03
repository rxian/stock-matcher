import { useState, useEffect } from 'react';
import {Header, Label} from "semantic-ui-react";
import './MentionedWith.scss';
import API from "../../api";
import {Link} from "react-router-dom";

function MentionedWith({ listingID }) {
    const [mentionedWithData, setMentionedWithData] = useState([]);

    useEffect(() => {
        API.get(`/api/listings/${listingID}/mentioned-with`).then((res) => {
            setMentionedWithData(res.data.data);
        }).catch((e) => {
            setMentionedWithData([]);
        });
    }, [listingID]);

    return <div className="MentionedWith">
        <div className='header-bar'> <Header as="h3"> Mentioned With </Header> </div>
        <div className='labels'>
            { mentionedWithData.map((item, i) =>
                <div className="mentioned-with-company">
                    <Link to={`/listing/${item.listing_id}`}>
                        <Label>{item.name}</Label> for {item.connections} times
                    </Link>
                </div>
            )}
        </div>
    </div>
}

export default MentionedWith;