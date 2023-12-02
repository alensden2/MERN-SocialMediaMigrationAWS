import React from 'react';
import PropTypes from 'prop-types';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';

const styles = {
  paper: {
    padding: 16,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    maxWidth: 600,
    margin: 'auto',
    marginTop: 40,
  },
  analyticsItem: {
    marginTop: 16,
  },
  graphImage: {
    width: '100%', // Adjust the width as needed
    marginTop: 16,
  },
};

const DummyAnalyticsPage = ({ classes }) => {
  // Dummy analytics data
  const analytics = {
    client_dict: {
      '192.168.1.1': 5,
      '192.168.1.2': 10,
      '192.168.1.3': 7,
    },
    total_requests: 22,
    total_get_requests: 15,
    total_post_requests: 7,
  };

  return (
    <Paper className={classes.paper}>
      <Typography variant="h4" gutterBottom>
        Analytics
      </Typography>

      <div className={classes.analyticsItem}>
        <Typography variant="h6">IPs Interacted:</Typography>
        <ul>
          {Object.keys(analytics.client_dict).map((ip, index) => (
            <li key={index}>{ip}</li>
          ))}
        </ul>
      </div>

      <div className={classes.analyticsItem}>
        <Typography variant="h6">Total Requests: {analytics.total_requests}</Typography>
      </div>

      <div className={classes.analyticsItem}>
        <Typography variant="h6">Total GET Requests: {analytics.total_get_requests}</Typography>
      </div>

      <div className={classes.analyticsItem}>
        <Typography variant="h6">Total POST Requests: {analytics.total_post_requests}</Typography>
      </div>

      {/* Include your graph image */}
      <img
        className={classes.graphImage}
        src={'/Users/cynos/Downloads/Cloud Arch/TermProject/bargraph.png'} // Replace with the actual path or URL of your graph image
        alt="Graph"
      />
    </Paper>
  );
};

DummyAnalyticsPage.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(DummyAnalyticsPage);
