import {useState} from "react";
import {Button, Form, Input} from "semantic-ui-react";
import {defaultEndDate, defaultStartDate} from "../../static/hardCodeConfig";

function OptionsBar({ handleUpdateOptions }) {
    const [startDate, setStartDate] = useState(defaultStartDate);
    const [endDate, setEndDate] = useState(defaultEndDate);
    const [startDateError, setStartDateError] = useState(false);
    const [endDateError, setEndDateError] = useState(false);

    const handleOnSubmit = () => {
        if (startDate === "") setStartDateError(true);
        if (endDate === "") setEndDateError(true);
        if (startDate === "" || endDate === "") return;

        setStartDateError(false);
        setEndDateError(false);
        handleUpdateOptions(startDate, endDate);
    };

    return <Form onSubmit={handleOnSubmit}>
        <Form.Field
            inline
            required
            error={startDateError}>
            <label>Start Date</label>
            <Input
                name='startDate'
                value={startDate}
                onChange={(e, { value }) => setStartDate(value)}
            />
        </Form.Field>
        <Form.Field
            inline
            required
            error={endDateError}>
            <label>End Date</label>
            <Input
                name='endDate'
                value={endDate}
                onChange={(e, { value }) => setEndDate(value)}
            />
        </Form.Field>
        <Button type='submit'>Submit</Button>
    </Form>
}

export default OptionsBar;